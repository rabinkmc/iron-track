## Technical decisions

Core idea is to keep the codebase as simple as possible. This comes with constraints rather than using whole set of DRF features. However, one is allowed to have attributes in django models, use manager methods for table queries. 

1. Use of plain serializers 
   The job of serializer is to perform serialization and deserialization of data. Beyond that, it should not be used for any other purpose. Although verbose, it is clear and easy to understand. It also allows for easy debugging and testing.

2. Use of plain viewsets
   The model viewsets are very convenient but most of the time they are overwritten anyways. So, I find using plain viewsets much better. Almost all the views then share the same structure so it becomes easier to read and maintain over time.

3. Use of services
   The business logic should be contained in services. The benefit is that this makes it easier to reuse the functions.

## Objective

Create a backend service to track your gym progress. Starting out, the service should allow a user to create his exercises, log his workout. 


## Todo
- [X] Ability to track workouts with multiple exercises
- [X] Track workouts with multiple sets and repetitions
- [X] Ability to track workouts with different types of exercises (push, pull, leg)
- [ ] Add the ability to track body weight and other body measurements, nutrition, sleep
- [ ] Add visualization for the tracked data
