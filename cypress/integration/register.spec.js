/// <reference types="cypress" /> 

import scores from "../fixtures/postScores.json";
import scoresSetTwo from "../fixtures/postScoresSetTwo.json";
var faker = require("faker");

let session_Id;
let set_one_quizId;
let set_two_quizId;
let user;
const successMessage = "Successfully created user";
const badReqMessage1 = "Email and password must be included in the request body";
const alreadyRegisteredMessage = "Email already registered";
const badReqMessage2 = "Email and password must be included in the request body.";
const missingName = "Name is missing.";
const invalidQuizIdMessage = "Quiz ID is not a valid UUID4 format.";
const quizIdIsRequiredMessage = "Quiz UUID must be included to register."


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
            password: faker.internet.password(),
            quizId: set_one_quizId
        };

        cy.registerEndpoint(user).should((response) => {
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
        });

    });

    it("should register another user", () => {
        user = {
            firstName: faker.name.firstName(),
            lastName: faker.name.lastName(),
            email: faker.internet.email(),
            password: faker.internet.password(),
            quizId: set_one_quizId
        };

        cy.registerEndpoint(user).should((response) => {
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
        });
    });

    it("should handle if the user already exists", () => {
        user = {
            firstName: faker.name.firstName(),
            lastName: faker.name.lastName(),
            email: faker.internet.email(),
            password: faker.internet.password(),
            quizId: set_two_quizId
        };

        cy.registerEndpoint(user).then(() => {
            cy.registerEndpoint(user).should((response) => {
                expect(response.status).to.equal(401);
                expect(response.headers["content-type"]).to.equal("application/json");
                expect(response.body).to.be.a("object");
                expect(response.body).to.have.property("error");
                expect(response.body.error).to.satisfy(function (s) {
                    return s === alreadyRegisteredMessage;
                });
            });
        });
    });

    it("should handle a missing email", () => {
        user = {
            firstName: faker.name.firstName(),
            lastName: faker.name.lastName(),
            password: faker.internet.password(),
            quizId: set_one_quizId
        };

        cy.registerEndpoint(user).should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error).to.satisfy(function (s) {
                return s === badReqMessage1;
            });
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
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.satisfy(function (s) {
                return s === badReqMessage2;
            });
        });
    });

    it("should handle a missing body", () => {
        cy.registerEndpoint().should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error).to.satisfy(function (s) {
                return s === badReqMessage2;
            });
        });
    });

    it("should handle a missing firstName", () => {
        user = {
            lastName: faker.name.lastName(),
            email: faker.internet.email(),
            password: faker.internet.password(),
            quizId: set_one_quizId
        };

        cy.registerEndpoint(user).should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error, { timeout: 3000 }).to.satisfy(function (s) {
                return s === missingName;
            });
        });
    });

    it("should handle a missing lastName", () => {
        user = {
            firstName: faker.name.firstName(),
            email: faker.internet.email(),
            password: faker.internet.password(),
            quizId: set_one_quizId
        };

        cy.registerEndpoint(user).should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error).to.satisfy(function (s) {
                return s === missingName;
            });
        });
    });

    it("should handle a missing quizId", () => {
        user = {
            firstName: faker.name.firstName(),
            lastName: faker.name.lastName(),
            email: faker.internet.email(),
            password: faker.internet.password()
        };

        cy.registerEndpoint(user).should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error).to.satisfy(function (s) {
                return s === quizIdIsRequiredMessage;
            });
        });
    });
});
