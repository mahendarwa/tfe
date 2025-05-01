 - name: Set Feature Branch Name
        run: |
          BASE_NAME="feature-${{ github.event.inputs.ReleaseYear }}-${{ github.event.inputs.ReleaseMonth }}-${{ github.event.inputs.ReleaseDate }}"
          if [ -n "${{ github.event.inputs.ReleaseReference }}" ]; then
            FEATURE_BRANCH="${BASE_NAME}-${{ github.event.inputs.ReleaseReference }}"
          else
            FEATURE_BRANCH="${BASE_NAME}"
          fi
          echo "FEATURE_BRANCH=${FEATURE_BRANCH}" >> $GITHUB_ENV

      - name: Create and Push Feature Branch
        run: |
          git config --global user.name "c8x6k9"
          git config --global user.email "C8X6K9_Zilver@github.com"
          git remote -v
          git ls-remote origin
          git checkout -b $FEATURE_BRANCH
          git remote set-url origin https://x-access-token:${{ secrets.MY_GITHUB_TOKEN }}@github.com/zilvertonz/GBS_DAE_Python_ETL.git
          git push origin $FEATURE_BRANCH
