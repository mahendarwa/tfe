echo "TERADATA_PASSWORD=\"${{ secrets.PRD_PASSWORD }}\"" >> $GITHUB_ENV

echo "Raw password: [$TERADATA_PASSWORD]"
echo "Password length: ${#TERADATA_PASSWORD}"

