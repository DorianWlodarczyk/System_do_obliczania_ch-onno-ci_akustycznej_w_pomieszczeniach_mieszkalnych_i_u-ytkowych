json_schema  = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "wymiar_pomieszczenia": {
      "type": "object",
      "properties": {
        "szerokosc": {
          "type": "number"
        },
        "dlugosc": {
          "type": "number"
        },
        "wysokosc": {
          "type": "number"
        }
      },
      "required": [
        "szerokosc",
        "dlugosc",
        "wysokosc"
      ]
    },
    "norma_id": {
      "type": "integer"
    },
    "elementy": {
      "type": "object",
      "properties": {
        "sufit": {
          "type": "array",
          "items": [
            {
              "type": "object",
              "properties": {
                "id": {
                  "type": "integer"
                },
                "powierzchnia": {
                  "type": "number"
                }
              },
              "required": [
                "id",
                "powierzchnia"
              ]
            }
          ]
        },
        "podloga": {
          "type": "array",
          "items": [
            {
              "type": "object",
              "properties": {
                "id": {
                  "type": "integer"
                },
                "powierzchnia": {
                  "type": "number"
                }
              },
              "required": [
                "id",
                "powierzchnia"
              ]
            }
          ]
        },
        "scianalewa": {
          "type": "array",
          "items": [
            {
              "type": "object",
              "properties": {
                "id": {
                  "type": "integer"
                },
                "powierzchnia": {
                  "type": "number"
                }
              },
              "required": [
                "id",
                "powierzchnia"
              ]
            }
          ]
        },
        "scianaprawa": {
          "type": "array",
          "items": [
            {
              "type": "object",
              "properties": {
                "id": {
                  "type": "integer"
                },
                "powierzchnia": {
                  "type": "number"
                }
              },
              "required": [
                "id",
                "powierzchnia"
              ]
            }
          ]
        },
        "scianafrontowa": {
          "type": "array",
          "items": [
            {
              "type": "object",
              "properties": {
                "id": {
                  "type": "integer"
                },
                "powierzchnia": {
                  "type": "number"
                }
              },
              "required": [
                "id",
                "powierzchnia"
              ]
            }
          ]
        },
        "scianatylna": {
          "type": "array",
          "items": [
            {
              "type": "object",
              "properties": {
                "id": {
                  "type": "integer"
                },
                "powierzchnia": {
                  "type": "number"
                }
              },
              "required": [
                "id",
                "powierzchnia"
              ]
            }
          ]
        },
        "inne": {
          "type": "array",
          "items": [
            {
              "type": "object",
              "properties": {
                "id": {
                  "type": "integer"
                },
                "powierzchnia": {
                  "type": "number"
                }
              },
              "required": [
                "id",
                "powierzchnia"
              ]
            }
          ]
        }
      },
      "required": [
        "sufit",
        "podloga",
        "scianalewa",
        "scianaprawa",
        "scianafrontowa",
        "scianatylna",
        "inne"
      ]
    }
  },
  "required": [
    "wymiar_pomieszczenia", 
    "elementy",
    "norma_id"
  ]
}