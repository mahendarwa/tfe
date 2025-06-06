const versionForUrl = versionString.replaceAll('.', '-');
const swaggerUrl = `${baseUrls[env]}-${versionForUrl}${domains[env]}/ae/swagger-ui/index.html`;
