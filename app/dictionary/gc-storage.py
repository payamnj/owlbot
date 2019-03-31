from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting, clean_name


class OwlBotGCStorage(GoogleCloudStorage):
    custom_domain = setting('GS_CUSTOM_DOMAIN')

    def url(self, name):
        """
        Return public url or a signed url for the Blob.
        This DOES NOT check for existance of Blob - that makes codes too slow
        for many use cases.
        """
        name = self._normalize_name(clean_name(name))
        blob = self.bucket.blob(self._encode_name(name))

        if self.custom_domain:
            return '{}/{}'.format(self.custom_domain, name)
        if self.default_acl == 'publicRead':
            return blob.public_url
        return blob.generate_signed_url(self.expiration)