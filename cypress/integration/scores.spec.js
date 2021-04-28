/// <reference types="cypress" />

import scores from "../fixtures/postScores.json";
import scoresAllTheSame from "../fixtures/postScoresAllSameAnswer.json";
import scoresSetTwo from "../fixtures/postScoresSetTwo.json";

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

  it("can post both sets of scores", () => {
    // Write Tests
    cy.request("POST", "/scores", scoresSetTwo).should((response) => {
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
      expect(response.body.valueScores).to.have.length(10);
      const { personalValues } = response.body;
      const { valueScores } = response.body;
      // P Values have all the right properties
      personalValues.forEach((value) => {
        expect(value).to.have.property("id");
        expect(value).to.have.property("description");
        expect(value).to.have.property("shortDescription");
        expect(value).to.have.property("name");
      });
      // Scores have all the right properties and valid values
      valueScores.forEach((score) => {
        expect(score).to.have.property("personalValue");
        expect(score).to.satisfy(function (s) {
          const isValid =
            typeof s.score === "number" && s.score >= 0 && s.score <= 10;
          return isValid;
        });
      });
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

  it("When the user answers the same for every question each value should be scored in the middle of the range", () => {
    //Post scores with all the same answer
    cy.request("POST", "/scores", scoresAllTheSame).should((response) => {
      sessionId = response.body["sessionId"];

      // Check the personal values scores for the corresponding sessions are correct
      cy.request(
        `http://localhost:5000/personal_values?session-id=${sessionId}`
      ).should((response) => {
        expect(response.status).to.equal(200);
        // Each personal value has a score in the middle of the range.
        const { valueScores } = response.body;
        valueScores.forEach((score) => {
          expect(score).to.have.property("personalValue");
          expect(score.score).to.equal(3);
        });
      });
    });
  });
});
