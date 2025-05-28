- name: Trigger Main Workflow in External Repository and Monitor Result
  uses: actions/github-script@v6
  with:
    github-token: ${{ secrets.WORKFLOW_TOKEN }}
    script: |
      const owner = "niq-enterprise";
      const repo = "panel-pod-aks-deploy";
      const workflow_id = "main.yml";
      const ref = "main";

      const now = new Date();
      const pad = n => n.toString().padStart(2, '0');
      const day = pad(now.getDate());
      const month = pad(now.getMonth() + 1);
      const year = now.getFullYear().toString().slice(-2);
      const hour = now.getHours();
      const versionString = `${day}.${month}.${year}.${hour}`;

      const inputs = {
        releasename: "usdev-deploy",
        releaseversion: versionString,
        operation: "deploy"
      };

      await github.rest.actions.createWorkflowDispatch({
        owner,
        repo,
        workflow_id,
        ref,
        inputs
      });

      const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
      let runId;
      let runFound = false;
      let attempt = 0;

      console.log("Waiting for workflow run to start...");
      while (!runFound && attempt < 20) {
        const { data: runs } = await github.rest.actions.listWorkflowRuns({
          owner,
          repo,
          workflow_id,
          branch: ref,
          event: "workflow_dispatch"
        });

        const matchingRun = runs.workflow_runs.find(run =>
          run.head_branch === ref && run.status !== "completed"
        );

        if (matchingRun) {
          runId = matchingRun.id;
          runFound = true;
          console.log(`Found workflow run with ID: ${runId}`);
        } else {
          await sleep(15000);
          attempt++;
        }
      }

      if (!runFound) {
        throw new Error("Remote workflow run not found.");
      }

      let status = "in_progress";
      let conclusion = null;

      while (status !== "completed") {
        const { data: run } = await github.rest.actions.getWorkflowRun({
          owner,
          repo,
          run_id: runId
        });

        status = run.status;
        conclusion = run.conclusion;
        console.log(`Workflow run status: ${status}`);

        if (status !== "completed") {
          await sleep(15000);
        }
      }

      console.log(`Workflow run completed with conclusion: ${conclusion}`);
      if (conclusion !== "success") {
        throw new Error(`Remote workflow failed with status: ${conclusion}`);
      }

      // ✅ SUCCESS: Now check if Swagger URL returns 200
      const execSync = require('child_process').execSync;
      console.log("✅ Remote job succeeded. Now checking Swagger URL...");
      try {
        const statusCode = execSync('curl -s -o /dev/null -w "%{http_code}" https://aggengapi-usqa.azure-omnsho-np.nielsencsp.net/ae/swagger-ui/index.html').toString().trim();
        console.log("Status code:", statusCode);
        if (statusCode !== "200") {
          throw new Error(`❌ URL is not accessible (status ${statusCode})`);
        } else {
          console.log("✅ URL is accessible");
        }
      } catch (err) {
        throw new Error(`Swagger URL check failed: ${err.message}`);
      }
