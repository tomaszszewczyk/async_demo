#include <stdio.h>
#include <unistd.h>
#include <sys/poll.h>

void handle_stdin(void) {
    char buffer[1000];
    fgets(buffer, sizeof(buffer), stdin);
    printf("user input %s\n", buffer);
}

void handle_timeout(void) {
    printf("timeout!!!\n");
}

int main(void) {
    struct pollfd fds[] = {
        {
            .fd = STDIN_FILENO,
            .events = POLLIN,
        }
    };

    while(1) {
        int ret = poll(fds, 1, 1000);

        if(ret == 0) {
            handle_timeout();
        } else if(fds[0].revents & POLLIN) {
            handle_stdin();
        }
    }
}
