package wiz

default result = "fail"

result = "pass" {
    input.tags[_].key.shortName == "costcenter"
    input.tags[_].values[_].shortName != null

  input.tags[_].key.shortName == "appname"
    input.tags[_].values[_].shortName != null
}

currentConfiguration := sprintf("IaC - Project tags does not exist or is empty:", [count(input.tags[_].key)])
expectedConfiguration := sprintf("IaC - Project tags should not be empty:", [count(input.tags[_].values[_])])
