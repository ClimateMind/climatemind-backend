/// <reference types="cypress" />

import scores from "../fixtures/postScores.json";

let sessionId; // store the session id from the post to chech we can retreive the values and scores.

describe("Scores endpoint", () => {
  it("can Post Scores", () => {
    // Write Tests
    cy.request("POST", "/scores", scores).should((response) => {
      expect(response.status).to.equal(201);
      expect(response.headers["content-type"]).to.equal("application/json");
      expect(response.headers["access-control-allow-origin"]).to.equal("*");
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("sessionId");
      expect(response.body.sessionId).to.be.a("string");
      sessionId = response.body["sessionId"];
    });
  });

  it("retreive the personal values for those scores", () => {
    cy.request(
      `http://localhost:5000/personal_values?session-id=${sessionId}`
    ).should((response) => {
      expect(response.status).to.equal(200);
      expect(response.headers["content-type"]).to.equal("application/json");
      expect(response.headers["access-control-allow-origin"]).to.equal("*");
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("personalValues");
    });
  });

  it("retreive the climate feed for those scores", () => {
    cy.request(`http://localhost:5000/feed?session-id=${sessionId}`).should(
      (response) => {
        expect(response.status).to.equal(200);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.headers["access-control-allow-origin"]).to.equal("*");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("climateEffects");
      }
    );
  });

  it("It accepts a null zip code", () => {
    const newScores = { ...scores, zipCode: null };
    cy.request("POST", "/scores", newScores).should((response) => {
      expect(response.status).to.equal(201);
      expect(response.headers["content-type"]).to.equal("application/json");
      expect(response.headers["access-control-allow-origin"]).to.equal("*");
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("sessionId");
      expect(response.body.sessionId).to.be.a("string");
    });
  });
});
