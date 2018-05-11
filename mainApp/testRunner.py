from django.test.runner import DiscoverRunner


class TestRunner(DiscoverRunner):
    def teardown_databases(self, old_config, **kwargs):
        """Destroy all the non-mirror databases."""
        pass
        # _teardown_databases(
        #     old_config,
        #     verbosity=self.verbosity,
        #     parallel=self.parallel,
        #     keepdb=self.keepdb,
        # )
