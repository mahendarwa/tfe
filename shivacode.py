- name: Create GitHub Release using CLI
  run: |
    cd GBS_DAE_OSS
    echo "Build version: ${{ env.FEATURE_BUILD_VERSION }}"

    gh release create "${{ env.FEATURE_BUILD_VERSION }}" ../odms-teradata-release.tgz \
      --title "Release ${{ env.FEATURE_BUILD_VERSION }}" \
      --notes "Automated Teradata build for ${{ github.event.inputs.feature_branch }}. Build version: ${{ env.FEATURE_BUILD_VERSION }}"
