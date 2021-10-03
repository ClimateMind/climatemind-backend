/// <reference types="cypress" /> 

import scores from "../fixtures/postScores.json";
import scoresSetTwo from "../fixtures/postScoresSetTwo.json";
var faker = require("faker");

let session_Id;
let set_one_quizId;
let set_two_quizId;
let user;
const successMessage = "Successfully created user";
const badReqMessage = "email must be included in the request body.";
const alreadyRegisteredMessage = "Cannot register email. Email already exists in the database.";
const missingPasswordMessage = "password must be included in the request body.";
const missingName = "Name is missing.";
const invalidQuizIdMessage = "Quiz ID is not a valid UUID4 format.";
const quizIdIsRequiredMessage = "Quiz UUID must be included to register."
const rateLimitPerSecond = "ratelimit exceeded 5 per 1 second";
const rateLimitPerMinute = "ratelimit exceeded 10 per 1 minute";
const rateLimitPerHour = "ratelimit exceeded 50 per 1 hour";
const rateLimitPerDay = "ratelimit exceeded 100 per 1 day";
const missingBodyMessage = "JSON body must be included in the request.";
const missingFirstNameMessage = "firstName must be included in the request body."
const missingLastNameMessage = "lastName must be included in the request body.";
const missingQuizIdMessage = "quizId must be included in the request body.";

describe("'/register' endpoint", () => {
    before(() => {
        cy.sessionEndpoint().should((response) => {
            session_Id = response.body.sessionId
        }).then(() => {
            cy.scoresEndpoint(scores, session_Id).should((response) => {
                set_one_quizId = response.body.quizId;
            });
            cy.scoresEndpoint(scoresSetTwo, session_Id).should((response) => {
                set_two_quizId = response.body.quizId;
            });
        })
    });

    it("should register a user", () => {
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
                expect(response.headers["content-type"]).to.equal(
                    "application/json"
                );
                expect(response.headers["access-control-allow-origin"]).to.equal(
                    "http://0.0.0.0:3000"
                );
                expect(response.body).to.be.a("object");
                expect(response.body).to.have.property("message");
                expect(response.body.message).to.satisfy(function (s) {
                    return s === successMessage;
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

    it("should register another user", () => {
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
                expect(response.headers["content-type"]).to.equal(
                    "application/json"
                );
                expect(response.headers["access-control-allow-origin"]).to.equal(
                    "http://0.0.0.0:3000"
                );
                expect(response.body).to.be.a("object");
                expect(response.body).to.have.property("message");
                expect(response.body.message).to.satisfy(function (s) {
                    return s === successMessage;
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

    it("should handle if the user already exists", () => {
        user = {
            firstName: faker.name.firstName(),
            lastName: faker.name.lastName(),
            email: faker.internet.email(),
            password: `@7${faker.internet.password()}`,
            quizId: set_two_quizId
        };

        cy.registerEndpoint(user).then(() => {
            cy.registerEndpoint(user).should((response) => {
                if (response.status == 401) {
                    expect(response.status).to.equal(409);
                    expect(response.headers["content-type"]).to.equal("application/json");
                    expect(response.body).to.be.a("object");
                    expect(response.body).to.have.property("error");
                    expect(response.body.error).to.satisfy(function (s) {
                        return s === alreadyRegisteredMessage;
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
    });

    it("should handle a missing email", () => {
        user = {
            firstName: faker.name.firstName(),
            lastName: faker.name.lastName(),
            password: `@7${faker.internet.password()}`,
            quizId: set_one_quizId
        };

        cy.registerEndpoint(user).should((response) => {
            if (response.status == 400) {
                expect(response.status).to.equal(400);
                expect(response.headers["content-type"]).to.equal("application/json");
                expect(response.body).to.be.a("object");
                expect(response.body).to.have.property("error");
                expect(response.body.error).to.be.a("string");
                expect(response.body.error).to.satisfy(function (s) {
                    return s === badReqMessage;
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

    it("should handle a missing password", () => {
        user = {
            firstName: faker.name.firstName(),
            lastName: faker.name.lastName(),
            email: faker.internet.email(),
            quizId: set_one_quizId
        };

        cy.registerEndpoint(user).should((response) => {
            if (response.status == 400) {
                expect(response.status).to.equal(400);
                expect(response.headers["content-type"]).to.equal("application/json");
                expect(response.body).to.be.a("object");
                expect(response.body).to.have.property("error");
                expect(response.body.error).to.satisfy(function (s) {
                    return s === missingPasswordMessage;
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

    it("should handle a missing body", () => {
        cy.registerEndpoint().should((response) => {
            if (response.status == 400) {
                expect(response.status).to.equal(400);
                expect(response.headers["content-type"]).to.equal("application/json");
                expect(response.body).to.be.a("object");
                expect(response.body).to.have.property("error");
                expect(response.body.error).to.be.a("string");
                expect(response.body.error).to.satisfy(function (s) {
                    return s === missingBodyMessage; 
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

    it("should handle a missing firstName", () => {
        user = {
            lastName: faker.name.lastName(),
            email: faker.internet.email(),
            password: `@7${faker.internet.password()}`,
            quizId: set_one_quizId
        };

        cy.registerEndpoint(user).should((response) => {
            if (response.status == 400) {
                expect(response.status).to.equal(400);
                expect(response.headers["content-type"]).to.equal("application/json");
                expect(response.body).to.be.a("object");
                expect(response.body).to.have.property("error");
                expect(response.body.error).to.be.a("string");
                expect(response.body.error, { timeout: 3000 }).to.satisfy(function (s) {
                    return s === missingFirstNameMessage;
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

    it("should handle a missing lastName", () => {
        user = {
            firstName: faker.name.firstName(),
            email: faker.internet.email(),
            password: `@7${faker.internet.password()}`,
            quizId: set_one_quizId
        };

        cy.registerEndpoint(user).should((response) => {
            if (response.status == 400) {
                expect(response.status).to.equal(400);
                expect(response.headers["content-type"]).to.equal("application/json");
                expect(response.body).to.be.a("object");
                expect(response.body).to.have.property("error");
                expect(response.body.error).to.be.a("string");
                expect(response.body.error).to.satisfy(function (s) {
                    return s === missingLastNameMessage;
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

    it("should handle a missing quizId", () => {
        user = {
            firstName: faker.name.firstName(),
            lastName: faker.name.lastName(),
            email: faker.internet.email(),
            password: `@7${faker.internet.password()}`
        };

        cy.registerEndpoint(user).should((response) => {
            if (response.status == 400) {
                expect(response.status).to.equal(400);
                expect(response.headers["content-type"]).to.equal("application/json");
                expect(response.body).to.be.a("object");
                expect(response.body).to.have.property("error");
                expect(response.body.error).to.be.a("string");
                expect(response.body.error).to.satisfy(function (s) {
                    return s === missingQuizIdMessage;
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
});
