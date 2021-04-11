/// <reference types="cypress" />

// Expected error responses
const badLoginMessage = "Wrong username or password";
const invalidReqMessage =
  "Email and password must included in the request body";

describe("User can login", () => {
  it("User can login", () => {
    // Register Test User
    const testUser = {
      email: "login@example.com",
      password: "password",
    };
    cy.request("POST", "http://localhost:5000/register", testUser);

    cy.request("POST", "http://localhost:5000/login", testUser).should(
      (response) => {
        expect(response.status).to.equal(200);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("access_token");
        expect(response.body).to.have.property("user");
        expect(response.body.access_token).to.satisfy(function (s) {
          return typeof s === "string";
        });
      }
    );
  });

  it("It handles incorrect credentials", () => {
    const invalidUser = {
      email: "invalid@example.com",
      password: "password",
    };
    cy.request("POST", "http://localhost:5000/login", invalidUser).should(
      (response) => {
        expect(response.status).to.equal(401);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.satisfy(function (s) {
          return s === badLoginMessage;
        });
      }
    );
  });
  it("It handles invalid email", () => {
    const body = {
      email: 1,
      password: "password",
    };
    cy.request("POST", "http://localhost:5000/login", body).should(
      (response) => {
        expect(response.status).to.equal(401);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.satisfy(function (s) {
          return s === badLoginMessage;
        });
      }
    );
  });
  it("It handles missing email", () => {
    const body = {
      password: "password",
    };
    cy.request("POST", "http://localhost:5000/login", body).should(
      (response) => {
        expect(response.status).to.equal(400);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.satisfy(function (s) {
          return s === invalidReqMessage;
        });
      }
    );
  });
  it("It handles missing password", () => {
    const body = {
      email: "login@example.com",
    };
    cy.request("POST", "http://localhost:5000/login", body).should(
      (response) => {
        expect(response.status).to.equal(400);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.satisfy(function (s) {
          return s === invalidReqMessage;
        });
      }
    );
  });
});
