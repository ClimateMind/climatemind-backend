/// <reference types="cypress" />
import scores from "../fixtures/postScores.json";

import {
  generateFirstName,
  generateLastName,
  generateEmail,
  generatePassword,
} from "./utils/generateRandomUsers";

// Expected error responses
const badLoginMessage = "Wrong email or password. Try again.";
const invalidReqMessage =
  "Email and password must be included in the request body";

const missingPassword =
  "Email and password must be included in the request body.";
let session_Id;
let quiz_Id;

describe("Login Tests", () => {
  it("User can login", function () {
    cy.request({
      method: "POST",
      url: "http://localhost:5000/session",
    }).then(function (response) {
      session_Id = response.body.sessionId;
      cy.request({
        method: "POST",
        url: "http://localhost:5000/scores",
        body: scores,
        headers: {
          "content-type": "application/json",
          "X-Session-Id": session_Id,
        },
      }).then((response) => {
        quiz_Id = response.body.quizId;

        const user1 = {
          firstName: generateFirstName(5),
          lastName: generateLastName(6),
          email: `${generateEmail(5)}@example.com`,
          password: generatePassword(5),
          quizId: quiz_Id,
        };
        cy.request("POST", "http://localhost:5000/register", user1)
          .should((response) => {
            expect(response.status).to.equal(201);
          })
          .then(() => {
            const user1_Login = {
              email: user1.email,
              password: user1.password,
            };
            cy.request(
              "POST",
              "http://localhost:5000/login",
              user1_Login
            ).should((response) => {
              expect(response.status).to.equal(200);
              expect(response.headers["content-type"]).to.equal(
                "application/json"
              );
              expect(response.headers["access-control-allow-origin"]).to.equal(
                "http://0.0.0.0:3000"
              );
              expect(response.body).to.be.a("object");
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
      });
    });
  });

  it("It handles incorrect credentials", function () {
    cy.request({
      method: "POST",
      url: "http://localhost:5000/session",
    }).then(function (response) {
      session_Id = response.body.sessionId;
      cy.request({
        method: "POST",
        url: "http://localhost:5000/scores",
        body: scores,
        headers: {
          "content-type": "application/json",
          "X-Session-Id": session_Id,
        },
      }).then((response) => {
        quiz_Id = response.body.quizId;

        const user1 = {
          firstName: generateFirstName(5),
          lastName: generateLastName(6),
          email: `${generateEmail(5)}@example.com`,
          password: generatePassword(5),
          quizId: quiz_Id,
        };
        cy.request("POST", "http://localhost:5000/register", user1)
          .should((response) => {
            expect(response.status).to.equal(201);
          })
          .then(() => {
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
      });
    });
  });

  it("It handles invalid email", function () {
    cy.request({
      method: "POST",
      url: "http://localhost:5000/session",
    }).then(function (response) {
      session_Id = response.body.sessionId;
      cy.request({
        method: "POST",
        url: "http://localhost:5000/scores",
        body: scores,
        headers: {
          "content-type": "application/json",
          "X-Session-Id": session_Id,
        },
      }).then((response) => {
        quiz_Id = response.body.quizId;

        const user1 = {
          firstName: generateFirstName(5),
          lastName: generateLastName(6),
          email: `${generateEmail(5)}@example.com`,
          password: generatePassword(5),
          quizId: quiz_Id,
        };
        cy.request("POST", "http://localhost:5000/register", user1)
          .should((response) => {
            expect(response.status).to.equal(201);
          })
          .then(() => {
            const body = {
              email: 1,
              password: user1.password,
            };
            cy.request({
              url: "http://localhost:5000/login",
              method: "POST",
              body: body,
              failOnStatusCode: false,
            }).should((response) => {
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
      });
    });
  });

  it("It handles missing email", function () {
    cy.request({
      method: "POST",
      url: "http://localhost:5000/session",
    }).then(function (response) {
      session_Id = response.body.sessionId;
      cy.request({
        method: "POST",
        url: "http://localhost:5000/scores",
        body: scores,
        headers: {
          "content-type": "application/json",
          "X-Session-Id": session_Id,
        },
      }).then((response) => {
        quiz_Id = response.body.quizId;

        const user1 = {
          firstName: generateFirstName(5),
          lastName: generateLastName(6),
          email: `${generateEmail(5)}@example.com`,
          password: generatePassword(5),
          quizId: quiz_Id,
        };
        cy.request("POST", "http://localhost:5000/register", user1)
          .should((response) => {
            expect(response.status).to.equal(201);
          })
          .then(() => {
            const body = {
              password: user1.password,
            };
            cy.request({
              url: "http://localhost:5000/login",
              method: "POST",
              body: body,
              failOnStatusCode: false,
            }).should((response) => {
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
      });
    });
  });

  it("It handles missing password", function () {
    cy.request({
      method: "POST",
      url: "http://localhost:5000/session",
    }).then(function (response) {
      session_Id = response.body.sessionId;
      cy.request({
        method: "POST",
        url: "http://localhost:5000/scores",
        body: scores,
        headers: {
          "content-type": "application/json",
          "X-Session-Id": session_Id,
        },
      }).then((response) => {
        quiz_Id = response.body.quizId;

        const user1 = {
          firstName: generateFirstName(5),
          lastName: generateLastName(6),
          email: `${generateEmail(5)}@example.com`,
          password: generatePassword(5),
          quizId: quiz_Id,
        };
        cy.request("POST", "http://localhost:5000/register", user1)
          .should((response) => {
            expect(response.status).to.equal(201);
          })
          .then(() => {
            const body = {
              email: user1.email,
            };
            cy.request({
              url: "http://localhost:5000/login",
              method: "POST",
              body: body,
              failOnStatusCode: false,
            }).should((response) => {
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
      });
    });
  });

  it("It handles invalid password", function () {
    cy.request({
      method: "POST",
      url: "http://localhost:5000/session",
    }).then(function (response) {
      session_Id = response.body.sessionId;
      cy.request({
        method: "POST",
        url: "http://localhost:5000/scores",
        body: scores,
        headers: {
          "content-type": "application/json",
          "X-Session-Id": session_Id,
        },
      }).then((response) => {
        quiz_Id = response.body.quizId;

        const user1 = {
          firstName: generateFirstName(5),
          lastName: generateLastName(6),
          email: `${generateEmail(5)}@example.com`,
          password: generatePassword(5),
          quizId: quiz_Id,
        };
        cy.request("POST", "http://localhost:5000/register", user1)
          .should((response) => {
            expect(response.status).to.equal(201);
          })
          .then(() => {
            const body = {
              email: user1.email,
              password: "@ClimateMind1234!",
            };
            cy.request({
              url: "http://localhost:5000/login",
              method: "POST",
              body: body,
              failOnStatusCode: false,
            }).should((response) => {
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
      });
    });
  });
  it("It handles missing credentials", function () {
    cy.request({
      method: "POST",
      url: "http://localhost:5000/session",
    }).then(function (response) {
      session_Id = response.body.sessionId;
      cy.request({
        method: "POST",
        url: "http://localhost:5000/scores",
        body: scores,
        headers: {
          "content-type": "application/json",
          "X-Session-Id": session_Id,
        },
      }).then((response) => {
        quiz_Id = response.body.quizId;

        const user1 = {
          firstName: generateFirstName(5),
          lastName: generateLastName(6),
          email: `${generateEmail(5)}@example.com`,
          password: generatePassword(5),
          quizId: quiz_Id,
        };
        cy.request("POST", "http://localhost:5000/register", user1)
          .should((response) => {
            expect(response.status).to.equal(201);
          })
          .then(() => {
            cy.request({
              url: "http://localhost:5000/login",
              method: "POST",
              failOnStatusCode: false,
            }).should((response) => {
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
      });
    });
  });

  it.only("handles too many requests", () => {});
});

