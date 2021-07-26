# Don't get bored app

## Objective

Please get familiar with the project's tasks described below, and the code that was introduced
by some developer in order to fulfill the requirements described in tasks.

Later on you will be asked to perform a **live code review** of the changes introduced by a developer
while sharing your screen.

## Tasks

Below are the tasks that the developer have implemented in the corresponding Pull Requests.

### Task #1

Build a RESTful API allowing to create, edit and list fun activities to be performed some day.
An activity should consist of the following fields:

- `description`
- `type` - one of the following:
    - `education`
    - `recreational`
    - `social`
    - `diy`
    - `charity`
    - `cooking`
    - `relaxation`
    - `music`
    - `busywork`
- `number of participants` - 1 or more
- `cost` - indicative from 1 to 10, where 1 is *"free"* and 10 is *"very expensive"*
- `date and time of adding`

It should be possible to mark an activity as **already performed**.

Also, it should be possible to filter out performed tasks and to sort them by `type`, `description` and
`creation date/time`.

### Task #2

Create an endpoint that would allow the user to auto-generate an activity when the user cannot come up with anything.
Use [boredapi.com][1] for auto-generating the activity.

## The code

Take a look at the Pull Requests. At this stage please don't focus on the details of the implementation.
Try to get a general idea of the project's structure and get familiar with the code. 

> **Hint:** Imagine you're a lead developer responsible for this project and think of all the things that you would pay
> attention to in order to comply with the best coding standards and development workflow.

[1]: http://boredapi.com/ "Bored API"