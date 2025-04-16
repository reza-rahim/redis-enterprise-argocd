**GitOps** is a modern way to do DevOps using Git as the single source of truth for managing infrastructure and application configurations.

### Here's the idea in simple terms:
- Everything is in Git: Your entire system configuration—like Kubernetes manifests, Helm charts, app settings—is stored in a Git repository.
- Declarative and version-controlled: You declare what the system should look like in Git (e.g., “I want 3 replicas of this app”), and Git keeps a history of every change.
- Automated synchronization: A GitOps tool (like Argo CD or Flux) constantly compares what’s in Git to what’s actually running (e.g., in Kubernetes). If there’s a difference, it updates the live environment to match Git—or alerts you.

### Key Benefits of GitOps:
- Consistency & Reliability: Environments can be replicated exactly (like staging = prod).
- Auditability: Every change is logged through Git commits and pull requests.
- Automation: CI/CD pipelines can automatically deploy changes as soon as they’re approved and merged.
- Rollback friendly: If something breaks, you can roll back just by reverting a Git commit.

### Tools Often Used in GitOps:
- Git (of course)
- Kubernetes
- Argo CD / Flux
- Helm (optional)
- Kustomize (optional)

### Visual:

   <img src="/images/argoCD.png" width="800">

<br>**links** 
- [What Is Argo CD?](https://argo-cd.readthedocs.io/en/stable/)
- [Solving configuration drift using GitOps with Argo CD](https://www.cncf.io/blog/2020/12/17/solving-configuration-drift-using-gitops-with-argo-cd/)


