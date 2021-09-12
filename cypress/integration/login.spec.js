/// <reference types="cypress" />

import scores from "../fixtures/postScores.json";
var faker = require("faker");

// Expected error responses
const successMessage = "Successfully created user";
const badLoginMessage = "Wrong email or password. Try again.";
const invalidReqMessage1 =
  "Email and password must be included in the request body";
const invalidReqMessage2 =
  "Email and password must be included in the request body.";
const rateLimitPerSecond = "ratelimit exceeded 5 per 1 second";
const rateLimitPerMinute = "ratelimit exceeded 10 per 1 minute";
const rateLimitPerHour = "ratelimit exceeded 50 per 1 hour";
const rateLimitPerDay = "ratelimit exceeded 100 per 1 day";

let session_Id;
let set_one_quizId;
let user;
let user_validCredentials;
let user_invalidCredentials;
let user_invalidEmail;
let user_missingEmail;
let user_missingPassword;
let user_invalidPassword;
let errorMessage;

describe("'/login' endpoint", () => {
  beforeEach(() => {
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
          password: `@7${faker.internet.password()}`,
          quizId: set_one_quizId
        };
        cy.registerEndpoint(user).should((response) => {
          if (response.status == 201) {
            expect(response.status).to.equal(201);
            expect(response.body.message).to.satisfy(function (s) {
              return s === successMessage;
            });
          } else {
            expect(response.status).to.equal(429);
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            errorMessage = response.body;
            if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
              expect(response.body.error).to.satisfy(function (s) {
                return s === rateLimitPerSecond;
              });
            } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
              expect(response.body.error).to.satisfy(function (s) {
                return s === rateLimitPerMinute;
              });
            } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
              expect(response.body.error).to.satisfy(function (s) {
                return s === rateLimitPerHour;
              });
            }
            else expect(response.body.error).to.satisfy(function (s) {
              return s === rateLimitPerDay;
            });
          }
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
      if (response.status == 200) {
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

      }
      else if (response.status == 429) {
        expect(response.body.error).to.be.a("string");
        expect(response.status).to.equal(429);
        expect(response.body).to.have.property("error");
        let errorMessage = response.body;
        if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerSecond;
          });
        } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerMinute;
          });
        } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerHour;
          });
        }
        else expect(response.body.error).to.satisfy(function (s) {
          return s === rateLimitPerDay;
        });
      } else {
        expect(response.status).to.equal(401);
        expect(response.body.message).to.satisfy(function (s) {
          return s === badLoginMessage;
        });
      }
    });
  });

  it("should handle incorrect credentials", () => {
    user_invalidCredentials = {
      email: "invalid@example.com",
      password: "@Invalid1password",
    };
    cy.loginEndpoint(user_invalidCredentials).should((response) => {
      if (response.status == 401) {
        expect(response.status).to.equal(401);
        expect(response.headers["content-type"]).to.equal(
          "application/json"
        );
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.satisfy(function (s) {
          return s === badLoginMessage;
        });

      } else {
        expect(response.status).to.equal(429);
        expect(response.body).to.have.property("error");
        let errorMessage = response.body;
        if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerSecond;
          });
        } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerMinute;
          });
        } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerHour;
          });
        }
        else expect(response.body.error).to.satisfy(function (s) {
          return s === rateLimitPerDay;
        });
      }
    });
  });

  it("should handle invalid email", () => {
    user_invalidEmail = {
      email: "invalid@example.com",
      password: user.password
    };
    cy.loginEndpoint(user_invalidEmail).should((response) => {
      if (response.status == 401) {
        expect(response.status).to.equal(401);
        expect(response.headers["content-type"]).to.equal(
          "application/json"
        );
        expect(response.body).to.be.an("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.satisfy(function (s) {
          return s === badLoginMessage;
        });

      } else {
        expect(response.status).to.equal(429);
        expect(response.body).to.have.property("error");
        let errorMessage = response.body;
        if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerSecond;
          });
        } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerMinute;
          });
        } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerHour;
          });
        }
        else expect(response.body.error).to.satisfy(function (s) {
          return s === rateLimitPerDay;
        });
      }
    });
  });

  it("should handle missing email", () => {
    user_missingEmail = {
      password: user.password
    };
    cy.loginEndpoint(user_missingEmail).should((response) => {
      if (response.status == 400) {
        expect(response.status).to.equal(400);
        expect(response.headers["content-type"]).to.equal(
          "application/json"
        );
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.be.a("string");
        expect(response.body.error).to.satisfy(function (s) {
          return s === invalidReqMessage1;
        });

      } else {
        expect(response.status).to.equal(429);
        expect(response.body).to.have.property("error");
        let errorMessage = response.body;
        if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerSecond;
          });
        } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerMinute;
          });
        } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerHour;
          });
        }
        else expect(response.body.error).to.satisfy(function (s) {
          return s === rateLimitPerDay;
        });
      }
    });
  });

  it("should handle missing password", () => {
    user_missingPassword = {
      email: user.email
    };
    cy.loginEndpoint(user_missingPassword).should((response) => {
      if (response.status == 400) {
        expect(response.status).to.equal(400);
        expect(response.headers["content-type"]).to.equal(
          "application/json"
        );
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.be.a("string");
        expect(response.body.error).to.satisfy(function (s) {
          return s === invalidReqMessage2;
        });

      } else {
        expect(response.body.error).to.be.a("string");
        expect(response.status).to.equal(429);
        expect(response.body).to.have.property("error");
        let errorMessage = response.body;
        if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerSecond;
          });
        } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerMinute;
          });
        } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerHour;
          });
        }
        else expect(response.body.error).to.satisfy(function (s) {
          return s === rateLimitPerDay;
        });
      }
    });
  });

  it("should handle invalid password", () => {
    user_invalidPassword = {
      email: user.email,
      password: "@ClimateMind1234!"
    };
    cy.loginEndpoint(user_invalidPassword).should((response) => {
      if (response.status == 401) {
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

      } else {
        expect(response.status).to.equal(429);
        expect(response.body).to.have.property("error");
        let errorMessage = response.body;
        if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerSecond;
          });
        } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerMinute;
          });
        } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerHour;
          });
        }
        else expect(response.body.error).to.satisfy(function (s) {
          return s === rateLimitPerDay;
        });
      }
    });
  });

  it("should handle missing credentials", () => {
    cy.loginEndpoint().should((response) => {
      if (response.status == 400) {
        expect(response.status).to.equal(400);
        expect(response.headers["content-type"]).to.equal(
          "application/json"
        );
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.satisfy(function (s) {
          return s === invalidReqMessage2;
        });

      } else {
        expect(response.status).to.equal(429);
        expect(response.body).to.have.property("error");
        let errorMessage = response.body;
        if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerSecond;
          });
        } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerMinute;
          });
        } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerHour;
          });
        }
        else expect(response.body.error).to.satisfy(function (s) {
          return s === rateLimitPerDay;
        });
      }
    });
  });

  //it.only("should handles too many requests", () => {});
});
