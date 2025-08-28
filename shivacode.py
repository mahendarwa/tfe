package wiz

import data.generic.cloud as cloudLib

default result = "pass"

result = "fail" {
    some j
    input.bucketEncryptionConfiguration.ServerSideEncryptionConfiguration.Rules[j].BucketKeyEnabled = false
}

result = "fail" {
    some j
    not cloudLib.isNullOrEmpty(
        input.bucketEncryptionConfiguration.ServerSideEncryptionConfiguration.Rules[j].ApplyServerSideEncryptionByDefault.KMSMasterKeyID
    )
}

result = "fail" {
    some j
    input.bucketEncryptionConfiguration.ServerSideEncryptionConfiguration.Rules[j].ApplyServerSideEncryptionByDefault.SSEAlgorithm != "AES256"
}
