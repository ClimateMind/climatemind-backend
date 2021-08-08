/// <reference types="cypress" /> 
import postScores from "../fixtures/postScores.json";
import scores from "../fixtures/postScores.json";

import { generateFirstName, generateLastName, generateEmail, generatePassword } from './utils/generateRandomUsers';

const successMessage = "Successfully created user";
const badReqMessage = "Email and password must be included in the request body";
const alreadyRegisteredMessage = "Email already registered";
const missingPassword = "Email and password must be included in the request body.";
let session_Id;
let quiz_Id;

describe("User Registration", () => {
    it('can register a user', function () {
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/session',
        }).then(function (response) {
            session_Id = response.body.sessionId
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/scores',
                body: scores,
                headers: {
                    'content-type': 'application/json',
                    'X-Session-Id': session_Id
                },

            }).then((response) => {
                quiz_Id = response.body.quizId;
                const user1 = {
                    firstName: generateFirstName(5),
                    lastName: generateLastName(6),
                    email: `${generateEmail(5)}@example.com`,
                    password: generatePassword(5),
                    quizId: quiz_Id
                };
                cy.request("POST", "http://localhost:5000/register", user1).should(
                    (response) => {
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
                    }
                );
            });
        });


    });

    it('Can register another user', function () {
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/session',
        }).then(function (response) {
            session_Id = response.body.sessionId
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/scores',
                body: postScores,
                headers: {
                    'content-type': 'application/json',
                    'X-Session-Id': session_Id
                },

            }).then((response) => {
                quiz_Id = response.body.quizId;
                const user2 = {
                    firstName: generateFirstName(5),
                    lastName: generateLastName(6),
                    email: `${generateEmail(5)}@example.com`,
                    password: generatePassword(20),
                    quizId: quiz_Id
                };

                cy.request("POST", "http://localhost:5000/register", user2).should(
                    (response) => {
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
                    }
                );
            });
        });


    });

    it('It handles if the user already exists', function () {
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/session',
        }).then(function (response) {
            session_Id = response.body.sessionId
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/scores',
                body: postScores,
                headers: {
                    'content-type': 'application/json',
                    'X-Session-Id': session_Id
                },

            }).then((response) => {
                quiz_Id = response.body.quizId;

                const user2 = {
                    firstName: generateFirstName(5),
                    lastName: generateLastName(6),
                    email: `${generateEmail(5)}@example.com`,
                    password: generatePassword(20),
                    quizId: quiz_Id
                };
                cy.request("POST", "http://localhost:5000/register", user2).should(
                    (response) => {
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
                    }
                );
                cy.request({
                    url: "http://localhost:5000/register",
                    method: "POST",
                    body: user2,
                    failOnStatusCode: false,
                }).should((response) => {
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
    });

    it('should handle a missing email', function () {
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/session',
        }).then(function (response) {
            session_Id = response.body.sessionId
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/scores',
                body: postScores,
                headers: {
                    'content-type': 'application/json',
                    'X-Session-Id': session_Id
                },
            }).then((response) => {
                quiz_Id = response.body.quizId;
                const user3 = {
                    firstName: generateFirstName(5),
                    lastName: generateLastName(6),
                    password: generatePassword(8),
                    quizId: quiz_Id
                };
                cy.request({
                    url: "http://localhost:5000/register",
                    method: "POST",
                    body: user3,
                    failOnStatusCode: false,
                }).should(
                    (response) => {
                        expect(response.status).to.equal(400);
                        expect(response.headers["content-type"]).to.equal("application/json");
                        expect(response.body).to.be.a("object");
                        expect(response.body).to.have.property("error");
                        expect(response.body.error).to.be.a("string");
                        expect(response.body.error).to.satisfy(function (s) {
                            return s === badReqMessage;
                        });
                    }
                );
            });
        });
    });

    it('should handle a missing password', function () {
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/session',
        }).then(function (response) {
            session_Id = response.body.sessionId
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/scores',
                body: postScores,
                headers: {
                    'content-type': 'application/json',
                    'X-Session-Id': session_Id
                },
            }).then((response) => {
                quiz_Id = response.body.quizId;
                const user4 = {
                    firstName: generateFirstName(5),
                    lastName: generateLastName(6),
                    email: `${generateEmail(5)}@example.com`,
                    quizId: quiz_Id
                };
                cy.request({
                    url: "http://localhost:5000/register",
                    method: "POST",
                    body: user4,
                    failOnStatusCode: false,
                }).should(
                    (response) => {
                        expect(response.status).to.equal(400);
                        expect(response.headers["content-type"]).to.equal("application/json");
                        expect(response.body).to.be.a("object");
                        expect(response.body).to.have.property("error");
                        expect(response.body.error).to.satisfy(function (s) {
                            return s === missingPassword;
                        });
                    }
                );
            });
        });
    });

    it('should handle a missing body', function () {
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/session',
        }).then(function (response) {
            session_Id = response.body.sessionId
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/scores',
                body: postScores,
                headers: {
                    'content-type': 'application/json',
                    'X-Session-Id': session_Id
                },

            }).then((response) => {
                quiz_Id = response.body.quizId;

                cy.request({
                    url: "http://localhost:5000/register",
                    method: "POST",
                    failOnStatusCode: false,
                }).should(
                    (response) => {
                        expect(response.status).to.equal(400);
                        expect(response.headers["content-type"]).to.equal("application/json");
                        expect(response.body).to.be.a("object");
                        expect(response.body).to.have.property("error");
                        expect(response.body.error).to.be.a("string");
                        expect(response.body.error).to.satisfy(function (s) {
                            return s === missingPassword;
                        });
                    }
                );
            });
        });
    });
});
