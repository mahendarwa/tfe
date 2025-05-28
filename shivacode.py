 - name: Check if Swagger URL returns 200
        run: |
          STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://aggengapi-usqa.azure-omnsho-np.nielsencsp.net/ae/swagger-ui/index.html)
          echo "Status code: $STATUS_CODE"
          if [ "$STATUS_CODE" -ne 200 ]; then
            echo "❌ URL is not accessible (status $STATUS_CODE)"
            exit 1
          else
            echo "✅ URL is accessible"
          fi
