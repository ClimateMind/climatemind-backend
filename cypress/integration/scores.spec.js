/// <reference types="cypress" />

import scores from "../fixtures/postScores.json";
import scoresSetTwo from "../fixtures/postScoresSetTwo.json";

let set_one_quizId;
let X_Session_Id;
let session_Id;
const uuid_Format = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/;

describe("Scores Two", () => {
    beforeEach(() => {
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/session',
        }).then(function (response) {
            //expect(response.body).property('sessionId').to.be.a('string')
            session_Id = response.body.sessionId
            expect(response.body.sessionId).to.eq(session_Id)
        });
    });

    it('can post one set of scores', function () {
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/scores',
            body: scores,
            headers: {
                'content-type': 'application/json',
                'X-Session-Id': session_Id
            },

        }).then((response) => {
            expect(response.status).to.equal(201);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.headers["access-control-allow-origin"]).to.equal("*");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("quizId");
            expect(response.body.quizId).to.be.a("string");
            expect(response.body.quizId).to.match(uuid_Format);
            //quizId = response.body["quizId"];
        });
    });

    it('can post both sets of scores', function () {
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/scores',
            body: scoresSetTwo,
            headers: {
                'content-type': 'application/json',
                'X-Session-Id': session_Id
            },

        }).then((response) => {
            expect(response.status).to.equal(201);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.headers["access-control-allow-origin"]).to.equal("*");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("quizId");
            expect(response.body.quizId).to.be.a("string");
            expect(response.body.quizId).to.match(uuid_Format);
            //quizId = response.body["quizId"];
        });
    });

});
