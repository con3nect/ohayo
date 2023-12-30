const testJson = {
  "tagName": "地域管辖",
  "attrs": {
      "fill": "green"
  },
  "children": [
      {
          "tagName": "专属管辖",
          "attrs": {
              "fill": "red"
          },
          "children": []
      },
      {
          "tagName": "特殊地域管辖",
          "attrs": {
              "fill": "red"
          },
          "children": []
      },
      {
          "tagName": "一般地域管辖",
          "attrs": {
              "fill": "green"
          },
          "children": [
              {
                  "tagName": "一般地域管辖一般情形",
                  "attrs": {
                      "fill": "green"
                  },
                  "children": [
                    {
                        "tagName": "一般地域管辖二般情形",
                        "attrs": {
                            "fill": "green"
                        },
                        "children": []
                    },
                    {
                        "tagName": "一般地域管辖三般情形",
                        "attrs": {
                            "fill": "green"
                        },
                        "children": []
                    }
                  ]
              }
          ]
      }
  ]
}
export default testJson 