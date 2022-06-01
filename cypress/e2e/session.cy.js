/// <reference types="cypress" />

const uuid_Format = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/;
describe("'/session' endpoint", () => {
    it("response of session endpoint should have a sessionId", () => {
        cy.sessionEndpoint().should((response) => {
            expect(response.status).to.equal(201);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.headers["access-control-allow-origin"]).to.equal("*");
            expect(response.body).to.be.an("object");
            expect(response.body).to.have.property("sessionId");
            expect(response.body.sessionId).to.be.a("string");
            expect(response.body.sessionId).to.match(uuid_Format);
            expect((Object.keys(response.body).length)).to.eq(1);
        });
    });
});
