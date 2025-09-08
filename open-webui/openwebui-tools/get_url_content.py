"""
author: Trenton
requirements: trafilatura, aiohttp, yarl, dnspython
version: 0.2.1
"""

import re
from typing import Dict
from aiohttp import ClientSession, TCPConnector
from yarl import URL
import trafilatura
import ipaddress
import dns.resolver
import dns.asyncresolver

class Tools:
    """
    URL Content Retrieval and Extraction - External Resource Content Extractor Tool
    Given a URL, fetches (GET) and extracts the full main content (not just a summary) of the web page.
    Use this tool to get the complete readable text from any external resource such as
    research / news articles, blog posts, documentation, or other web pages.
    """

    def __init__(self):
        self.citation = True

    async def extract_resource_content(self, url: str) -> Dict[str, any]:
        """
        Extract the content from an external resource (URL / URI / link).
        :param url: The URL of the external resource / page / link to extract.
        :return: Dictionary of the data components. The content of the external resource (extracted), or an error message if extraction fails.
        """
        try:
            # Convert to HTTPS if not already
            # Do not allow relative path only requests and do not allow requests to current instance
            # URL must be HTTPS by default even if provided HTTP
            url_obj = URL(url)
            if (
                not url_obj.scheme
                or url_obj.scheme == "http"
                or url_obj.scheme != "https"
            ):
                try:
                    try:
                        url_obj.scheme = "https"
                    except Exception as ie:
                        print(f"URL handling exception assigning scheme as https: {ie}")

                    url_obj = URL(f"https://{url}")

                    if (
                        not url_obj.scheme
                        or url_obj.scheme == "http"
                        or url_obj.scheme != "https"
                    ):
                        url_obj.scheme = "https"

                    # If still all else fails then do this
                    # (another consideration is removing scheme, using object's URL to then recreate new as https://, but that is unnecessary)
                    if url_obj.scheme and url_obj.scheme != "https":
                        url_obj = URL(url)
                        url_obj.scheme = "https"

                except Exception as e:
                    print(f"URL handling and HTTPS enablement exception: {e}")

            # Consider additional safety check on ports (if/when explicitly provided)
            # Basic port validation such as unsigned values (non-negative) is trivial to check
            # Not only due to range, but potential to use as a de facto port scanner
            # Or requests to IPs / Ports it does not have any place doing (especially for QUIC / UDP)

            def _is_private_ip(ip):
                """
                Check if an IP address is within RFC 1918 private ranges.
                """
                try:
                    # Check IPv4 addresses
                    ipv4 = ipaddress.IPv4Address(ip)
                    return (
                        (10 == ipv4.network_address[0])
                        or (172 >= ipv4.network_address[0] >= 16)
                        or (
                            192 == ipv4.network_address[0]
                            and 168 == ipv4.network_address[1]
                        )
                        or (127 == ipv4.network_address[0])
                        or (0 == ipv4.network_address[0])
                        or (
                            ipv4.network_address[0] > 255
                            or ipv4.network_address[1] > 255
                            or ipv4.network_address[2] > 255
                            or ipv4.network_address[3] > 255
                        )
                        # Consider mcast / bcast / link local / etc. ranges
                        # Also consider IPs used by cloud providers for special purposes
                    )
                except ipaddress.AddressValueError:
                    pass

                try:
                    # Check IPv6 addresses
                    ipv6 = ipaddress.IPv6Address(ip)
                    return ipv6.is_private or (
                        ipv6.ipv4_mapped and _is_private_ip(str(ipv6.ipv4_mapped))
                    )
                    # Also consider checking IPv6 discard prefix
                    # as well as link local, etc. to the extent applicable
                except ipaddress.AddressValueError:
                    pass

                return False

            # TODO: consider SVCB and other scenarios which may have port specific implications
            async def resolve_dns(host):
                """
                Resolve DNS records for a given hostname.

                This function returns a list of IP addresses associated with the hostname.
                It handles at least both A (IPv4) and AAAA (IPv6) record types.
                """
                resolved_addresses = []
                resolved_addresses_ipv6 = []
                if host:
                    try:
                        # Additional considerations for DNS sec operations
                        # Resolve IPv4 / IPv6 addresses through resolver lib
                        answers = await dns.asyncresolver.resolve(host, "A")
                        resolved_addresses = [answer.address for answer in answers]

                        answers = await dns.asyncresolver.resolve(host, "AAAA")
                        resolved_addresses_ipv6 = [answer.address for answer in answers]
                    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN) as e:
                        # Adapted as necessary
                        print(
                            f"DNS resolver no answer, NXDOMAIN, or similar. Exception: {e}"
                        )
                    except dns.resolver.Timeout as et:
                        raise Exception(f"DNS query timed out ({et})")
                    except Exception as e:
                        raise Exception(f"Error resolving DNS: {e}")

                    return {
                        "A": resolved_addresses or [],
                        "AAAA": resolved_addresses_ipv6 or [],
                    }

            # Validate URL is not a local/private resource
            host = (
                url_obj.host.lower()
            )  # Applying lowercase operations may be naive at best (reference standards)
            ip_match = re.match(r"^(\d{1,3}\.){3}\d{1,3}(:\d+)?$", host)  # IPv4 check

            if host != url_obj.host:
                print(
                    "Potential normalization applied to host for request (not an error)."
                )

            # TODO: hardening and ensure no "simple" hostnames or other reserved / internal domains can be utilized
            if (
                host == "localhost"
                or host == ""
                or host.endswith(".local")
                or host.endswith(".localhost")
                or host.endswith(".invalid")
                or host.endswith(".internal")
                or host.endswith(".arpa")
                or host.endswith(".test")
                or host.endswith(".example")
                or host.endswith(".bad")
                or host.endswith(".lan")
                or host.endswith(".localdomain")
                or host.endswith(".")
                or (host == "wpad" or host.endswith(".wpad"))
                # Check whether the client libraries support shorthand IPs (such as simple numbers which convert to an IP or omitted octets)
                # Or does not contain any FQDN (such as hostnames)
                or (ip_match and _is_private_ip(ip_match.group(0)))
                or re.match(r"^[0-9a-fA-F:]+$", host)  # IPv6 check
            ):
                return {
                    "message_error": "Invalid URL: Cannot access local/private networks or otherwise invalid domains."
                }

            # Potentially validate intermediate steps in resolving (CNAME records and other potential DNS rebinding implications)
            # Resolve DNS to get IP addresses
            try:
                addrs = await resolve_dns(host)
            except Exception as e:
                return f"DNS resolution failed for {host}: {e}"

            if not addrs or not isinstance(addrs, dict):
                return {
                    "message_error": "Unable to fulfill request. Domain name system resolution unsuccessful."
                }

            if any(_is_private_ip(ip) for ip in addrs):
                return {
                    "message_error": "Invalid URL: Cannot access local/private network addresses."
                }

            # Plan to ensure the request explicitly uses the resolved address related details accordingly
            # Fetch the content
            async with ClientSession(
                # connector=TCPConnector(resolver=preresolver)
                connector=TCPConnector()
            ) as session:
                response = await session.get(url_obj, allow_redirects=False)

                if not (200 <= response.status < 300):
                    if response.status in (300, 301, 302, 303, 307, 308):
                        location = response.headers.get("location") or ""
                        return {
                            "message_error": f"Redirected with HTTP status code {response.status} to: {location}",
                            "redirect": True,
                            "response_location": location,
                            "response_status_code": response.status,
                            "request_host": f"{host or ''}",
                            "http_method": "GET",
                        }
                        # Redirect loop scenario mitigation / protection?
                    else:
                        return {
                            "message_error": f"Failed to fetch page. Status code: {response.status}",
                            "redirect": False,
                        }

                try:
                    content_type = response.headers.get("Content-Type")
                    if "text/html" not in content_type:
                        if "application/json" in content_type:
                            downloaded = await response.json()
                        else:
                            downloaded = await response.text()
                            """
                            # Read the entire body in chunks
data = b''
while True:
    chunk = await response.content.read(1024) # Read 1KB at a time
    if not chunk:
        break
    data += chunk

    # Add overflow or maximum size (and timeout) check to abandon or other action

# Or use an async iterator (more common)
async for chunk in response.content:
    process(chunk) # Process each chunk as it arrives   
                            """
                        return {
                            "content_type": response.headers.get("Content-Type")
                            or "application/octet-stream",
                            "content": downloaded,
                            "message_error": f"Unsupported content type: {content_type}.",
                            "redirect": False,
                        }
                except Exception as e:
                    print(f"Raw content exception: {e}")

                    raise e

                downloaded = await response.text()

            # Extract main content
            main_text = ""
            title = ""
            extracted_content = trafilatura.extract(
                downloaded.encode(), url=str(url_obj)
            )

            try:
                if extracted_content and not isinstance(extracted_content, str):
                    extracted_content = extracted_content.as_dict()
            except Exception as err:
                print(f"extract as_dict call error: {err}")

            if isinstance(extracted_content, dict) and "content" in extracted_content:
                main_text = extracted_content["content"]
                if "title" in extracted_content:
                    title = extracted_content["title"]
            elif isinstance(extracted_content, str):
                main_text = extracted_content
                title = ""
            else:
                print("No relevant content for extraction.")

            meta = trafilatura.extract_metadata(downloaded.encode())

            try:
                if meta and not isinstance(meta, str):
                    meta = meta.as_dict()
            except Exception as err:
                print(f"extract_metadata as_dict call error: {err}")

            if isinstance(meta, dict) and "title" in meta:
                title = meta["title"]
            elif isinstance(meta, str):
                title = meta or ""

            desired_keys = {
                "author",
                "date",
                "filedate",
                "categories",
                "tags",
                "title",
                "description",
                "hostname",
                "url",
                "image",
                "sitename",
                "license",
            }

            # Filter the dictionary to include only the keys that exist in meta
            main_meta = {key: meta[key] for key in desired_keys if key in meta}

            if main_text:
                if "url" in main_meta:
                    meta_url = main_meta["url"] or str(url_obj)
                else:
                    meta_url = str(url_obj)

                meta_sitename = ""
                if "sitename" in main_meta:
                    meta_sitename = main_meta["sitename"] or title
                else:
                    if "hostname" in main_meta:
                        meta_sitename = main_meta["hostname"] or title

                main_meta["text"] = (
                    f"Content (Title: {title}) from [{meta_sitename}]({meta_url})\n\n{main_text}"
                )

                print(
                    f'URI (request):\t"{str(url_obj)}"\nURI (response):\t"{meta_url}"'
                )
            else:
                main_meta["text"] = str(meta) or None

            return main_meta
        except Exception as e:
            import traceback

            traceback.print_exc()
            return {"message_error": f"Skipping retrieval / extraction: {e}"}

    async def retrieve_external_resource(self, url: str) -> Dict[str, any]:
        """
        Retrieve an external resource (URL / URI / link).
        :param url: The URL of the external resource / page / link to retrieve and/or extract content from.
        :return: Dictionary of the data components. The content of the external resource (extracted or raw), or an error message if it does not succeed.
        """
        return await self.extract_resource_content(url)
