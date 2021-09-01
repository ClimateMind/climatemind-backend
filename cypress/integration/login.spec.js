/// <reference types="cypress" />

import scores from "../fixtures/postScores.json";
var faker = require("faker");

// Expected error responses
const badLoginMessage = "Wrong email or password. Try again.";
const invalidReqMessage =
  "Email and password must be included in the request body";

const missingPassword =
  "Email and password must be included in the request body.";

let session_Id;
let set_one_quizId;
let user;
let user_validCredentials;
let user_invalidCredentials;
let user_invalidEmail;
let user_missingEmail;
let user_missingPassword;
let user_invalidPassword;

describe("'/login' endpoint", () => {
  before(() => {
    cy.sessionEndpoint().should((response) => {
      session_Id = response.body.sessionId
    }).then(() => {
      cy.scoresEndpoint(scores, session_Id).should((response) => {
        set_one_quizId = response.body.quizId;
      }).then(() => {
        user = {
          firstName: faker.name.firstName(),
          lastName: faker.name.lastName(),
          email: faker.internet.email(),
          password: faker.internet.password(),
          quizId: set_one_quizId
        };
        cy.registerEndpoint(user).should((response) => {
          expect(response.status, { timeout: 500 }).to.equal(201, { timeout: 500 });
        });
      });
    });
  });

  it("should log a user in", () => {
    user_validCredentials = {
      "email": user.email,
      "password": user.password,
    };

    cy.loginEndpoint(user_validCredentials).should((response) => {
      expect(response.status).to.equal(200);
      expect(response.headers["content-type"]).to.equal(
        "application/json"
      );
      expect(response.headers["access-control-allow-origin"]).to.equal(
        "http://0.0.0.0:3000"
      );
      expect(response.body).to.be.an("object");
      expect(response.body).to.have.property("message");
      expect(response.body).to.have.property("access_token");
      expect(response.body).to.have.property("user");
      expect(response.body.message).to.satisfy(function (s) {
        return typeof s === "string";
      });
      expect(response.body.access_token).to.satisfy(function (s) {
        return typeof s === "string";
      });
      expect(response.body.user.first_name).to.be.an("string");
      expect(response.body.user.last_name).to.be.an("string");
      expect(response.body.user.email).to.be.an("string");
      expect(response.body.user.user_uuid).to.be.an("string");
      expect(response.body.user.quiz_id).to.be.an("string");
    });
  });

  it("should handle incorrect credentials", () => {
    user_invalidCredentials = {
      email: "invalid@example.com",
      password: "@Invalid1password",
    };
    cy.loginEndpoint(user_invalidCredentials).should((response) => {
      expect(response.status).to.equal(401);
      expect(response.headers["content-type"]).to.equal(
        "application/json"
      );
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("error");
      expect(response.body.error).to.satisfy(function (s) {
        return s === badLoginMessage;
      });
    });
  });

  it("should handle invalid email", () => {
    user_invalidEmail = {
      email: "invalid@example.com",
      password: user.password
    };
    cy.loginEndpoint(user_invalidEmail).should((response) => {
      expect(response.status).to.equal(401);
      expect(response.headers["content-type"]).to.equal(
        "application/json"
      );
      expect(response.body).to.be.an("object");
      expect(response.body).to.have.property("error");
      expect(response.body.error).to.satisfy(function (s) {
        return s === badLoginMessage;
      });
    });
  });

  it("should handle missing email", () => {
    user_missingEmail = {
      password: user.password
    };
    cy.loginEndpoint(user_missingEmail).should((response) => {
      expect(response.status).to.equal(400);
      expect(response.headers["content-type"]).to.equal(
        "application/json"
      );
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("error");
      expect(response.body.error).to.be.a("string");
      expect(response.body.error).to.satisfy(function (s) {
        return s === invalidReqMessage;
      });
    });
  });

  it("should handle missing password", () => {
    user_missingPassword = {
      email: user.email
    };
    cy.loginEndpoint(user_missingPassword).should((response) => {
      expect(response.status).to.equal(400);
      expect(response.headers["content-type"]).to.equal(
        "application/json"
      );
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("error");
      expect(response.body.error).to.be.a("string");
      expect(response.body.error).to.satisfy(function (s) {
        return s === missingPassword;
      });
    });
  });

  it("should handle invalid password", () => {
    user_invalidPassword = {
      email: user.email,
      password: "@ClimateMind1234!"
    };
    cy.loginEndpoint(user_invalidPassword).should((response) => {
      expect(response.status).to.equal(401);
      expect(response.headers["content-type"]).to.equal(
        "application/json"
      );
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("error");
      expect(response.body.error).to.be.a("string");
      expect(response.body.error).to.satisfy(function (s) {
        return s === badLoginMessage;
      });
    });
  });

  it("should handle missing credentials", () => {
    cy.loginEndpoint().should((response) => {
      expect(response.status).to.equal(400);
      expect(response.headers["content-type"]).to.equal(
        "application/json"
      );
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("error");
      expect(response.body.error).to.satisfy(function (s) {
        return (
          s ===
          "Email and password must be included in the request body."
        );
      });
    });
  });

  //it.only("should handles too many requests", () => {});
});
