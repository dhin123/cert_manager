# Certificate Manager

## High Level Architecture


This application uses a **microservice architecture** with the following services:

1. `api-service`: Acts as an API gateway and handles initial sanitization of validating schema and routing the requests to appropriate services.
2. `customer-service`: Handles the logic of creating and deleting customers and also takes care of persistence.
3. `cert-service`: Handles the logic of creating and activating certificates and listing all active certificates for a customer. This service also notifies the `notification-service` to send an email notification to an external system (http://httpbin.org) when a certificate status is updated.
4. `notification-service`: Sends email notifications when a certificate status is updated.

## Deployment
The containerized application is deployed on an **AWS EKS Cluster**.

## API Endpoints
The host for the endpoints is: `http://aa97153191598445199bd806e767797d-1812338798.us-west-1.elb.amazonaws.com`

### Customer Operations
- **Create a Customer** (POST `/v1/customer`)
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"name":"qet1344", "email":"this_worked@gmail.com", "password":"sss"}' /v1/customer
    ```
    Returns 201 on success, 400 when a customer already exists.

- **Delete a Customer** (DELETE `/customer/<customer_id>`)
    ```bash
    curl -X DELETE /customer/<customer_id>
    ```
    Returns 200 on success, Error codes: 400, 404.

### Certificate Operations
- **Create a Certificate** (POST `/v1/certificate`)
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{
      "commonName": "www.example.com",
      "organizationName": "Your Company Name",
      "localityName": "City Name",
      "stateOrProvinceName": "State Name",
      "countryName": "Country Code (2 letters)",
      "organizationalUnitName": "Department Name",
      "emailAddress": "freshstart@gmail.com",
      "customer_id": "7158648882976006143",
      "publicKey": "Your Public Key"
    }' /v1/certificate
    ```
    Returns 201 on success, Error codes: 404, 400.

- **Update Certificate Status** (PATCH `/v1/certificate/<certificate_id>`)
    ```bash
    curl -X PATCH -H "Content-Type: application/json" -d '{"status":"activate"}' /v1/certificate/<certificate_id>
    ```
    Returns 200 on success, Error codes: 404, 400.

- **Get All Active Certificates for a Customer** (GET `/v1/certificates/<customer_id>`)
    ```bash
    curl -X GET /v1/certificates/<customer_id>
    ```
    Returns 200 on success, Error codes: 404, 400.

Please replace `<customer_id>` and `<certificate_id>` with actual values when using these commands
