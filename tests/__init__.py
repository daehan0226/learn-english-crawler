# https://docs.pytest.org/en/6.2.x/fixture.html?
### Arrange
# where we prepare everything for our test.
# This can mean preparing objects, starting/killing services,
# entering records into a database, or even things like defining a URL to query,
# generating some credentials for a user that doesn’t exist yet,
# or just waiting for some process to finish.
#######
### Act
# the singular,
# state-changing action that kicks off the behavior we want to test.
# This behavior is what carries out the changing of the state of the system under test (SUT),
# and it’s the resulting changed state that we can look at to make a judgement about the behavior.
# This typically takes the form of a function/method call.
###########
### Assert
# where we look at that resulting state and check if it looks how we’d expect after the dust has settled.
# It’s where we gather evidence to say the behavior does or does not align with what we expect.
# The assert in our test is where we take that measurement/observation and apply our judgement to it.
# If something should be green, we’d say assert thing == "green".
###########
### Cleanup
# where the test picks up after itself, so other tests aren’t being accidentally influenced by it.
####
# At it’s core, the test is ultimately the act and assert steps,
# with the arrange step only providing the context.
# Behavior exists between act and assert.
