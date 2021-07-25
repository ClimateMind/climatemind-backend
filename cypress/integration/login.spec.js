/// <reference types="cypress" />
import postScores from "../fixtures/postScores.json";

// Expected error responses
const badLoginMessage = "Wrong email or password. Try again.";
const invalidReqMessage =
  "Email and password must included in the request body";

describe.only("User can login", () => {
  it("User can login", () => {
    // Register Test User
    const testUser = {
      firstName: "test",
      lastName: "user",
      email: "test4@example.com",
      password: "PassWord7!",
      quizId: "30d54be8-c7ff-43f9-bfb3-8d427bc6eefa",
    };

    // Post scores to register user
    cy.request("POST", "http://localhost:5000/scores", postScores).should(
      (response) => {
        testUser.quizId = response.body.quizId;

        // TODO: This test is horrible, tidy up when we have data seeding
        cy.request("POST", "http://localhost:5000/register", testUser).should(
          (response) => {
            cy.request("POST", "http://localhost:5000/login", testUser).should(
              (response) => {
                expect(response.status).to.equal(200);
                expect(response.headers["content-type"]).to.equal(
                  "application/json"
                );
                expect(
                  response.headers["access-control-allow-origin"]
                ).to.equal("http://0.0.0.0:3000");
                expect(response.body).to.be.a("object");
                expect(response.body).to.have.property("access_token");
                expect(response.body).to.have.property("user");
                expect(response.body.access_token).to.satisfy(function (s) {
                  return typeof s === "string";
                });
              }
            );
          }
        );
      }
    );
  });

  it("It handles incorrect credentials", () => {
    const invalidUser = {
      email: "invalid@example.com",
      password: "password",
    };
    cy.request({
      url: "http://localhost:5000/login",
      method: "POST",
      body: invalidUser,
      failOnStatusCode: false,
    }).should((response) => {
      expect(response.status).to.equal(401);
      expect(response.headers["content-type"]).to.equal("application/json");
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("error");
      expect(response.body.error).to.satisfy(function (s) {
        return s === badLoginMessage;
      });
    });
  });
  it("It handles invalid email", () => {
    const body = {
      email: 1,
      password: "password",
    };
    cy.request({
      url: "http://localhost:5000/login",
      method: "POST",
      body: body,
      failOnStatusCode: false,
    }).should((response) => {
      expect(response.status).to.equal(401);
      expect(response.headers["content-type"]).to.equal("application/json");
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("error");
      expect(response.body.error).to.satisfy(function (s) {
        return s === badLoginMessage;
      });
    });
  });
  it("It handles missing email", () => {
    const body = {
      password: "password",
    };
    cy.request({
      url: "http://localhost:5000/login",
      method: "POST",
      body: body,
      failOnStatusCode: false,
    }).should((response) => {
      expect(response.status).to.equal(400);
      expect(response.headers["content-type"]).to.equal("application/json");
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("error");
      expect(response.body.error).to.satisfy(function (s) {
        return s === invalidReqMessage;
      });
    });
  });
  it("It handles missing password", () => {
    const body = {
      email: "login@example.com",
    };
    cy.request({
      url: "http://localhost:5000/login",
      method: "POST",
      body: body,
      failOnStatusCode: false,
    }).should((response) => {
      expect(response.status).to.equal(401);
      expect(response.headers["content-type"]).to.equal("application/json");
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("error");
      expect(response.body.error).to.satisfy(function (s) {
        return s === badLoginMessage;
      });
    });
  });
});
