/// <reference types="cypress" />

import scores from "../fixtures/postScores.json";

let session_Id;
let set_one_quizId;
let Zip_Code;
let invalidZipCode = "The postcode provided is not valid.";

describe("'/post-code' endpoint", () => {

    beforeEach(() => {
        cy.sessionEndpoint().should((response) => {
            session_Id = response.body.sessionId
        }).then(() => {
            cy.scoresEndpoint(scores, session_Id).should((response) => {
                Zip_Code = scores.zipCode;
                set_one_quizId = response.body.quizId;
            })
        });
    });

    it("should submit Zip_Code with /post-code endpoint and response should have a quizId", () => {
        cy.postCodeEndpoint(Zip_Code, set_one_quizId).should((response) => {
            expect(response.status).to.equal(201);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.headers["access-control-allow-origin"])
                .to.equal("*");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("message");
            expect(response.body).to.have.property("postCode");
            expect(response.body).to.have.property("quizId");
            expect(response.body.quizId).to.be.a("string");
        });
    });

    it("can handle invalid post code", () => {
        cy.postCodeEndpoint("123", set_one_quizId).should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.headers["access-control-allow-origin"])
                .to.equal("*");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error).to.satisfy(function (s) {
                return s === invalidZipCode;
            });
        });
    });
});
