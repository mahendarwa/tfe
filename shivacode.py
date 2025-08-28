package wiz

import data.generic.cloud as cloudLib

default result = "pass"

result = "fail" {
    input.bucketEncryptionConfiguration.ServerSideEncryptionConfiguration.Rules[j].BucketKeyEnabled = false
}

result = "fail" {
    not cloudLib.isNullOrEmpty(input.bucketEncryptionConfiguration.ServerSideEncryptionConfiguration.Rules[j].ApplyServerSideEncryptionByDefault.KMSMasterKeyID)
}

result = "fail" {
    input.bucketEncryptionConfiguration.ServerSideEncryptionConfiguration.Rules[j].ApplyServerSideEncryptionByDefault.SSEAlgorithm != "AES256"
}
