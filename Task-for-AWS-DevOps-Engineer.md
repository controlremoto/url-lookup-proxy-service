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
    * The service consumes a "mocked" database right now, but in real scenario, this URLS would be stored and consumed from a cloud database. I'm not sure I get the question, but in case the direction of the question is about how to update the database with new urls, I would set up a process where users can submit new URLs to be analyzed. On the other hand, if the question is about how to update the service with new URLS, then we need a new route to handle the new URLS, and we can process the new URLS in batches and update the database.
* You’re woken up at 3am, what are some of the things you’ll look for in the app?
    * I think there is still something missing in the question. I will assume I have been woken up because the service is down.. in that case, I would first check the logs to see if there are any errors or issues that can be identified. If we integrate monitoring tools like cloudwatch, or custom logging solution, I would check the metrics to see if there is any unusual activity or spikes in metrics dashboard which could lead to a potential issue.
* Does that change anything you’ve done in the app?
    * I did not get the question.
* What are some considerations for the lifecycle of the app?
    * I think there is still something missing in the question. I will assume the question is about the lifecycle of the app in terms of development and maintenance. In that case, I would consider implementing a CI/CD pipeline to automate the testing and deployment process. Definietly I would set up steps such as unit testing, build, dependency checks, sast, image, dast and whichever scan as possible to cover security and quality of the code.
* You need to deploy a new version of this application. What would you do?
    * Short answer: Run the created pipeline.
    * Long answer: Once I have made changes to the codebase, and run local tests, I commit the changes to the git repository and the pipeline would run automatically and deploy to the development environment. After some tests, promote it to the production environment.
