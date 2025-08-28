package wiz

import data.generic.cloud as cloudLib

default result = "pass"

result = "fail" {
    some j
    rule := input.bucketEncryptionConfiguration.ServerSideEncryptionConfiguration.Rules[j]
    rule.BucketKeyEnabled = false
}

result = "fail" {
    some j
    rule := input.bucketEncryptionConfiguration.ServerSideEncryptionConfiguration.Rules[j]
    not cloudLib.isNullOrEmpty(rule.ApplyServerSideEncryptionByDefault.KMSMasterKeyID)
}

result = "fail" {
    some j
    rule := input.bucketEncryptionConfiguration.ServerSideEncryptionConfiguration.Rules[j]
    rule.ApplyServerSideEncryptionByDefault.SSEAlgorithm != "AES256"
}
