# 🔍 Choosing an issue to do

## How to find an issue to work on

{% hint style="success" %}
You are free to choose any unassigned issue to work on.&#x20;

If you are interested in an assigned issue which doesn't have any updates for a long time feel free to follow up in the comments.
{% endhint %}

### Issues workflow

We are using [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects) to manage the backend repository issues. Multiple views are presented. For example, a [board view](https://github.com/orgs/ClimateMind/projects/2/views/1?filterQuery=repo%3A%22ClimateMind%2Fclimatemind-backend%22) contains several pipelines with a workflow from left to right.

<figure><img src="../../.gitbook/assets/Screenshot 2022-10-18 at 23.42.09.png" alt=""><figcaption><p>Climate mind backend agile board</p></figcaption></figure>

* New issues will go into the `Backlog` pipeline.
* After prioritizing, the issue status will be changed to `To do`
* `In progress` pipeline contains issues currently in progress
* `In review` contains issues with a Pull Request
* `Done` pipeline contains issues that closed less than 21 days ago.

### Priority

#### Priority field

The priority field can be used to identify the most urgent issues. Use [filtration by priority ](https://github.com/orgs/ClimateMind/projects/2/views/1?filterQuery=repo%3A%22ClimateMind%2Fclimatemind-backend%22+priority%3A%22%F0%9F%8C%8B+Urgent%22)on the board view to see issues with specific priority, or use [table view](https://github.com/orgs/ClimateMind/projects/2/views/2?filterQuery=repo%3A%22ClimateMind%2Fclimatemind-backend%22) by priority.

<figure><img src="../../.gitbook/assets/Screenshot 2022-10-18 at 23.51.32.png" alt=""><figcaption><p>Filtration example</p></figcaption></figure>

{% hint style="info" %}
You could also filter by other fields like `assignee:, label:,` etc.
{% endhint %}

#### Issue position

There may be times when the repo doesn't contain any issues with priority tags. If so, the most urgent tasks tend to be at the top of the pipeline in the [board view](https://github.com/orgs/ClimateMind/projects/2/views/1?filterQuery=repo%3A%22ClimateMind%2Fclimatemind-backend%22).

#### Pipeline priority

The [To do](https://github.com/orgs/ClimateMind/projects/2/views/1?filterQuery=repo%3A%22ClimateMind%2Fclimatemind-backend%22+status%3A%22To+do%22) pipeline is the first place to look for an issue to work on. If it's empty check tasks in [Backlog](https://github.com/orgs/ClimateMind/projects/2/views/1?filterQuery=repo%3A%22ClimateMind%2Fclimatemind-backend%22+status%3A%22%F0%9F%93%8B+Backlog%22) pipeline.

## First Issue

Issues labelled with [good first issue](https://github.com/orgs/ClimateMind/projects/2/views/1?filterQuery=repo%3A%22ClimateMind%2Fclimatemind-backend%22+label%3A%22good+first+issue%22) are marked as a good start for newcomers.

{% hint style="success" %}
Feel free to ask any question directly in the issue comments.
{% endhint %}

## How to get started once you've chosen an issue

* comment on the issue you would like to take, we will then be able to assign it to you
* [do stuff](development/) in your local git repository :tools:
* push changes to your fork and [make a Pull Request](development/making-a-pr.md)
* make [Circle CI pass](development/ci-continuous-integration.md) successfully :white\_check\_mark:
* get approved :ballot\_box\_with\_check:&#x20;
* [feel good](https://i.giphy.com/media/BPJmthQ3YRwD6QqcVD/giphy.webp) :tada::earth\_americas:
