# Task for AWS DevOps Engineer

For this exercise, we would like to see how you go about solving a technical exercise with architecting for the future in mind. This is not a timed exercise, though we ask that you complete as promptly as you are able. It's important to us that you have the flexibility to provide a solution in the way that makes the most sense for your circumstances.  

For some points of reference, the range of time prior candidates with successful submissions have spent is between a couple of hours to around 40\. It's really up to you. Our assessment will not be based on how much total time you spend on the exercise, but rather how your solution aligns with your stated plan.

For Part 1 of the exercise, we suggest using Python or Go because our reviewers are most familiar with these languages but that is not a hard requirement. For Part 2, we do not expect you to do extensive research in order to formulate your responses. We prefer you answer based on your current level of experience. Use of LLM-based coding assistants or agents is up to you. Regardless of the tools you use, be prepared to answer questions about your submission, including sources of any code used.  

One of our key values in how we develop new systems is to start with simple implementations and progressively make them more capable, scalable and reliable.  

As you work through this exercise, please use a Git-based repository to commit your updates (Bitbucket, GitHub, etc). We’d like to see your development workflow using revision control. It's up to you how frequently you commit and what you decide to include in each push. **You can use whatever Git repo you want (even your own) as long as it’s accessible by us.**  

Please also include some tests for your project and instructions on how to get the application up and running. Assume we know nothing about how it needs to be run. Your solution should not rely on access to any specific cloud infrastructure. It should be runnable locally on macOS or Linux.  

Here's what we would like you to build:

**URL lookup service**  

We have an HTTP proxy that is scanning traffic looking for malware URLs. Before allowing HTTP connections to be made, this proxy asks a service that maintains several databases of malware URLs if the resource being requested is known to contain malware.  

## **Part 1:**

## Write a small web service that responds to GET requests where the caller passes in a URL and the service responds with some information about that URL

The GET requests would look like this:  

```bash
  GET /urlinfo/1/{hostname\_and\_port}/{original\_path\_and\_query\_string}  
```

The caller wants to know if it is safe to access that URL or not. As the implementer you get to choose the response format and structure. These lookups are blocking users from accessing the URL until the caller receives a response from your service.  

## **Part 2:**

## As a thought exercise, please describe how you would accomplish the following

* The size of the URL list could grow infinitely. How might you scale this beyond the memory capacity of the system?
    * If the size is reffered to the number of the URLS to be analyzed, depending on the requirement, I already added a rate limit to the solution, in addition I would add a cache layer so that the already analyzed URLs can be stored and accessed faster. Finally, the URL needs to be stored in a cloud database.
* Assume that the number of requests will exceed the capacity of a single system, describe how might you solve this, and how might this change if you have to distribute this workload to an additional region, such as Europe.
    * I would use a load balancer to distribute the incoming traffic to multiple instances of the service allowing us to scale the solution. In case we need to distribute this workload to an additional region, I would set up a multi-region cloud architecture with replication of the created services (DB, load balancer, etc).
* What are some strategies you might use to update the service with new URLs? Updates may be as much as 5 thousand URLs a day with updates arriving every 10 minutes.
    * I would implement a batch ingestion process that can handle frequent updates. This would involve a dedicated endpoint or background job to process incoming URL lists in bulk. In case of the dedicated endpoint approach, I would ensure the payload is properly validated and the processing is done asynchronously to avoid blocking the main service. For the background job approach, I would use a message queue to manage the updates and ensure they are processed in a timely manner.
* You’re woken up at 3am, what are some of the things you’ll look for in the app?
    * Assuming I have been alerted due to a service outage or degraded performance, my first step would be to check the application logs for errors or exceptions. I would also review monitoring dashboards for metrics such as request latency, error rates, and resource utilization. If integrated with tools like CloudWatch or a custom monitoring solution, I would look for unusual activity or spikes that could indicate the root cause of the issue.
* Does that change anything you’ve done in the app?
    * I would ensure that the application has sufficient logging and monitoring in place from the start. This includes structured logs, health checks, and integration with alerting systems to proactively detect and respond to issues.
* What are some considerations for the lifecycle of the app?
    * I would prioritize implementing a CI/CD pipeline to automate testing and deployment. This would include steps such as unit testing, build verification, dependency checks, static analysis (SAST), image scanning, and dynamic analysis (DAST) to maintain security and code quality throughout the application's lifecycle.
* You need to deploy a new version of this application. What would you do?
    * Short answer: Run the created pipeline.
    * Long answer: Once I have made changes to the codebase, and run local tests, I commit the changes to the git repository and the pipeline would run automatically and deploy to the development environment. After some tests, promote it to the production environment.
