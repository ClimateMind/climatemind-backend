/// <reference types="cypress" />

describe("'/questions' endpoint", () => {
    it("User should get Questions", () => {
        cy.questionsEndpoint()
            .should((response) => {
                expect(response.status).to.equal(200);
                expect(response.headers["content-type"])
                    .to.equal("application/json");
                expect(response.headers["access-control-allow-origin"])
                    .to.equal("*");
                expect(response.body).to.be.an("object");
                expect(response.body).to.have.property("SetOne");
                expect(response.body).to.have.property("SetTwo");
                expect(response.body).to.have.property("Answers");
                expect(response.body).to.have.property("Directions");
            });
    });

    it("SetOne questions should have the correct properties", () => {
        cy.questionsEndpoint()
            .should((response) => {
                expect(response.body.SetOne).to.be.an("array");
                expect(response.body.SetOne).to.have.length(10);
                for (var SetOneIndex in response.body.SetOne) {
                    expect(response.body.SetOne[SetOneIndex]).to.be.an("object");
                    expect(response.body.SetOne[SetOneIndex]).to.have.property("id");
                    expect(response.body.SetOne[SetOneIndex]).to.have.property("value");
                    expect(response.body.SetOne[SetOneIndex]).to.have.property("question");
                    expect(response.body.SetOne[SetOneIndex].id).to.be.a("number");
                    expect(response.body.SetOne[SetOneIndex].value).to.be.a("string");
                    expect(response.body.SetOne[SetOneIndex].question).to.be.a("string");
                }
            });
    });

    it("SetTwo questions should have the correct properties", () => {
        cy.questionsEndpoint()
            .should((response) => {
                expect(response.body.SetTwo).to.be.an("array");
                //expect((Object.keys(response.body.SetTwo).length)).to.eq(10);
                expect(response.body.SetTwo).to.have.length(10);
                for (var SetTwoIndex in response.body.SetTwo) {
                    expect(response.body.SetTwo[SetTwoIndex]).to.be.an("object");
                    expect(response.body.SetTwo[SetTwoIndex]).to.have.property("id");
                    expect(response.body.SetTwo[SetTwoIndex]).to.have.property("value");
                    expect(response.body.SetTwo[SetTwoIndex]).to.have.property("question");
                    expect(response.body.SetTwo[SetTwoIndex].id).to.be.a("number");
                    expect(response.body.SetTwo[SetTwoIndex].value).to.be.a("string");
                    expect(response.body.SetTwo[SetTwoIndex].question).to.be.a("string");
                }
            });

    });

    it("Answers should have the correct properties", () => {
        cy.questionsEndpoint()
            .should((response) => {
                expect(response.body.Answers).to.be.an("array");
                expect(response.body.Answers).to.have.length(6);
                for (var AnswersIndex in response.body.Answers) {
                    expect(response.body.Answers[AnswersIndex]).to.be.an("object");
                    expect(response.body.Answers[AnswersIndex]).to.have.property("id");
                    expect(response.body.Answers[AnswersIndex]).to.have.property("text");
                    expect(response.body.Answers[AnswersIndex].id).to.be.a("number");
                    expect(response.body.Answers[AnswersIndex].text).to.be.a("string");
                }
            });
    });

    it("Directions should have the correct properties", () => {
        cy.questionsEndpoint()
            .should((response) => {
                expect(response.body.Directions).to.be.a("string");
            })
    });
});
