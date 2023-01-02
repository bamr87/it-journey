# syntax=docker/dockerfile:1
# escape=\
# Directives as above need to be before comments and builder instruction.
# Documentation found here: https://docs.docker.com/engine/reference/builder/
FROM scratch
ADD hello /
CMD ["/hello"]

# Test run
RUN echo 'we are running some # of cool things'
