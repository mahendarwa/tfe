{
  "relationships": [
    {
      "type": [
        {
          "type": "USES"
        }
      ],
      "with": {
        "relationships": [
          {
            "type": [
              {
                "reverse": true,
                "type": "ENCRYPTS"
              }
            ],
            "with": {
              "select": true,
              "type": [
                "MANAGEMENT_SERVICE"
              ],
              "where": {
                "nativeType": {
                  "EQUALS": [
                    "Microsoft.Compute/diskEncryptionSets"
                  ]
                }
              }
            }
          }
        ],
        "select": true,
        "type": [
          "VOLUME"
        ]
      }
    }
  ],
  "select": true,
  "type": [
    "VIRTUAL_MACHINE"
  ],
  "where": {
    "cloudPlatform": {
      "EQUALS": [
        "Azure"
      ]
    }
  }
}
