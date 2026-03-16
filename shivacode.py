We are seeing Wiz flag openssl/libssl3@3.0.18-1~deb12u2 in our distroless images as vulnerable and recommending an upgrade to 3.0.19. However, Snyk does not report this issue.

According to Debian security notes, version 3.0.18-1~deb12u2 already contains the backported patch, so the vulnerability appears to be remediated at the OS level.

Could you please confirm if this should be treated as a false positive or if additional configuration is required?


Possible False Positive – OpenSSL vulnerability in Debian distroless image
