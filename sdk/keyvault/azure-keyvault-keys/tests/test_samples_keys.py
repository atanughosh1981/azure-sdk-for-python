# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
from __future__ import print_function
import functools
import hashlib
import os

from azure.core.exceptions import ResourceNotFoundError
from devtools_testutils import ResourceGroupPreparer, KeyVaultAccountPreparer
from keys_preparer import VaultClientPreparer
from keys_test_case import KeyVaultTestCase


def print(*args):
    assert all(arg is not None for arg in args)


def test_create_key_client():
    vault_url = "vault_url"
    # pylint:disable=unused-variable
    # [START create_key_client]

    from azure.identity import DefaultAzureCredential
    from azure.keyvault.keys import KeyClient

    # Create a KeyClient using default Azure credentials
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url, credential)

    # [END create_key_client]


class TestExamplesKeyVault(KeyVaultTestCase):

    @ResourceGroupPreparer(random_name_enabled=True)
    @KeyVaultAccountPreparer(enable_soft_delete=True)
    @VaultClientPreparer()
    def test_example_key_crud_operations(self, vault_client, **kwargs):
        from dateutil import parser as date_parse

        key_client = vault_client.keys
        # [START create_key]
        from dateutil import parser as date_parse

        expires_on = date_parse.parse("2050-02-02T08:00:00.000Z")

        # create a key with optional arguments
        key = key_client.create_key("key-name", "RSA-HSM", expires_on=expires_on)

        print(key.name)
        print(key.id)
        print(key.key_type)
        print(key.properties.expires_on)

        # [END create_key]
        # [START create_rsa_key]

        key_size = 2048
        key_ops = ["encrypt", "decrypt", "sign", "verify", "wrapKey", "unwrapKey"]

        # create an rsa key with size specification
        # RSA key can be created with default size of '2048'
        key = key_client.create_rsa_key("key-name", hardware_protected=True, size=key_size, key_operations=key_ops)

        print(key.id)
        print(key.name)
        print(key.key_type)
        print(key.key_operations)

        # [END create_rsa_key]
        # [START create_ec_key]
        key_curve = "P-256"

        # create an EC (Elliptic curve) key with curve specification
        # EC key can be created with default curve of 'P-256'
        ec_key = key_client.create_ec_key("key-name", curve=key_curve)

        print(ec_key.id)
        print(ec_key.properties.version)
        print(ec_key.key_type)
        print(ec_key.key.crv)

        # [END create_ec_key]
        # [START get_key]

        # get the latest version of a key
        key = key_client.get_key("key-name")

        # alternatively, specify a version
        key_version = key.properties.version
        key = key_client.get_key("key-name", key_version)

        print(key.id)
        print(key.name)
        print(key.properties.version)
        print(key.key_type)
        print(key.properties.vault_url)

        # [END get_key]
        # [START update_key]

        # update attributes of an existing key
        expires_on = date_parse.parse("2050-01-02T08:00:00.000Z")
        tags = {"foo": "updated tag"}
        updated_key = key_client.update_key_properties(key.name, expires_on=expires_on, tags=tags)

        print(updated_key.properties.version)
        print(updated_key.properties.updated_on)
        print(updated_key.properties.expires_on)
        print(updated_key.properties.tags)
        print(key.key_type)

        # [END update_key]
        # [START delete_key]

        # delete a key
        deleted_key_poller = key_client.begin_delete_key("key-name")
        deleted_key = deleted_key_poller.result()

        print(deleted_key.name)

        # if the vault has soft-delete enabled, the key's deleted_date,
        # scheduled purge date and recovery id are set
        print(deleted_key.deleted_date)
        print(deleted_key.scheduled_purge_date)
        print(deleted_key.recovery_id)

        # if you want to block until deletion is complete, call wait() on the poller
        deleted_key_poller.wait()

        # [END delete_key]

    @ResourceGroupPreparer(random_name_enabled=True)
    @KeyVaultAccountPreparer(enable_soft_delete=True)
    @VaultClientPreparer()
    def test_example_key_list_operations(self, vault_client, **kwargs):
        key_client = vault_client.keys

        for i in range(4):
            key_client.create_ec_key("key{}".format(i))
        for i in range(4):
            key_client.create_rsa_key("key{}".format(i))

        # [START list_keys]

        # get an iterator of keys
        keys = key_client.list_properties_of_keys()

        for key in keys:
            print(key.id)
            print(key.name)

        # [END list_keys]

        # [START list_properties_of_key_versions]

        # get an iterator of a key's versions
        key_versions = key_client.list_properties_of_key_versions("key-name")

        for key in key_versions:
            print(key.id)
            print(key.name)

        # [END list_properties_of_key_versions]

        # [START list_deleted_keys]

        # get an iterator of deleted keys (requires soft-delete enabled for the vault)
        deleted_keys = key_client.list_deleted_keys()

        for key in deleted_keys:
            print(key.id)
            print(key.name)
            print(key.scheduled_purge_date)
            print(key.recovery_id)
            print(key.deleted_date)

        # [END list_deleted_keys]

    @ResourceGroupPreparer(random_name_enabled=True)
    @KeyVaultAccountPreparer()
    @VaultClientPreparer()
    def test_example_keys_backup_restore(self, vault_client, **kwargs):
        key_client = vault_client.keys
        created_key = key_client.create_key("keyrec", "RSA")
        key_name = created_key.name
        # [START backup_key]

        # backup key
        key_backup = key_client.backup_key(key_name)

        # returns the raw bytes of the backed up key
        print(key_backup)

        # [END backup_key]

        polling_interval = 0 if self.is_playback() else 2

        key_client.begin_delete_key(key_name, _polling_interval=polling_interval).wait()

        # [START restore_key_backup]

        # restore a key backup
        restored_key = key_client.restore_key_backup(key_backup)
        print(restored_key.id)
        print(restored_key.properties.version)

        # [END restore_key_backup]

    @ResourceGroupPreparer(random_name_enabled=True)
    @KeyVaultAccountPreparer(enable_soft_delete=True)
    @VaultClientPreparer()
    def test_example_keys_recover(self, vault_client, **kwargs):
        key_client = vault_client.keys
        created_key = key_client.create_key("key-name", "RSA")
        polling_interval = 0 if self.is_playback() else 2
        key_client.begin_delete_key(created_key.name, _polling_interval=polling_interval).wait()
        # [START get_deleted_key]

        # get a deleted key (requires soft-delete enabled for the vault)
        deleted_key = key_client.get_deleted_key("key-name")
        print(deleted_key.name)

        # if the vault has soft-delete enabled, the key's deleted_date
        # scheduled purge date and recovery id are set
        print(deleted_key.deleted_date)
        print(deleted_key.scheduled_purge_date)
        print(deleted_key.recovery_id)

        # [END get_deleted_key]
        # [START recover_deleted_key]

        # recover a deleted key to its latest version (requires soft-delete enabled for the vault)
        recover_key_poller = key_client.begin_recover_deleted_key("key-name")
        recovered_key = recover_key_poller.result()
        print(recovered_key.id)
        print(recovered_key.name)

        # if you want to block until key is recovered server-side, call wait() on the poller
        recover_key_poller.wait()

        # [END recover_deleted_key]
