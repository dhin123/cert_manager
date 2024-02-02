# Certificate Manager

## High Level Architecture

<img width="1118" alt="Screenshot 2024-02-01 at 10 36 55 PM" src="https://github.com/dhin123/cert_manager/assets/50316763/fac3ba2a-05e5-446b-835b-8c4ff26677dd">


This application uses a **microservice architecture** with the following services:

1. `api-service`: Acts as an API gateway and handles initial sanitization of validating schema and routing the requests to appropriate services.
2. `customer-service`: Handles the logic of creating and deleting customers and also takes care of persistence.
3. `cert-service`: Handles the logic of creating and activating certificates and listing all active certificates for a customer. This service also notifies the `notification-service` to send an email notification to an external system (http://httpbin.org) when a certificate status is updated.
4. `notification-service`: Sends email notifications when a certificate status is updated.

## To Know
1. Currently, for a customer,  uniqueness is identified through the email_id provided. 
2. From coding challenge perspective, in create certificate schema, I am not persisting any data other than the ones mentioned in the coding challenge(	1	Belongs to one and only one Customer, Can be either active or inactive, Has a private key, Has a certificate body)
2. From coding challenge perspective, a certificate is will always be deactivated at the time of creation. 
3. From coding challenge perspective, deleting a customer with any associated certificates irrespective of certificate status is not possible.
4. From coding challenge perspective, activating and deactivating a certificate API only accepts “activate” and “deactivate” values

## Deployment
The containerized application is deployed on an **AWS EKS Cluster**.

## API Endpoints
The host for the endpoints is: `http://aa97153191598445199bd806e767797d-1812338798.us-west-1.elb.amazonaws.com`

### Customer Operations
- **Create a Customer** (POST `/v1/customer`)
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"name":"yourname", "email":"valid@email.com", "password":"yourpassword"}' /v1/customer
    ```
    Returns 201 on success, Error codes: 400, 404

- **Delete a Customer** (DELETE `/customer/<customer_id>`)
    ```bash
    curl -X DELETE /v1/customer/<customer_id>
    ```
    Returns 200 on success, Error codes: 400, 404

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
  "customer_id": "<customer_id>",
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
    curl -X GET /v1/certificates/customer_id 
    ```
    Returns 200 on success, Error codes: 404, 400.

Please replace `<customer_id>` and `<certificate_id>` with actual values when using these commands
