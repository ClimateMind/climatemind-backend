/// <reference types="cypress" />

describe("/myths endpoint", () => {
    it("should get myths", () => {
        cy.mythsEndpoint()
            .should((response) => {
                expect(response.status).to.equal(200);
                expect(response.headers["content-type"]).to.equal("application/json");
                expect(response.headers["access-control-allow-origin"]).to.equal("*");
                expect(response.body).to.be.an("object");
                expect(response.body).to.have.property("myths");
                expect(response.body.myths).to.be.an("array");
                expect(response.body.myths).to.not.have.length(0);
            });
    });

    it("should get correct myths with correct properties", () => {
        cy.mythsEndpoint().should((response) => {
            const myths = response.body.myths;
            myths.forEach((myth) => {
                expect(myth).to.have.property("faultyLogicDescription");
                expect(myth).to.have.property("iri");
                expect(myth).to.have.property("mythClaim");
                expect(myth).to.have.property("mythRebuttal");
                expect(myth).to.have.property("mythSources");
                expect(myth).to.have.property("mythTitle");
                expect(myth).to.have.property("mythVideos");
                expect(myth.faultyLogicDescription).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
                expect(myth.iri).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
                expect(myth.mythClaim).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
                expect(myth.mythRebuttal).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
                expect(myth.mythSources).to.satisfy(function (s) {
                    return s === null || Array.isArray(s)
                });
                expect(myth.mythTitle).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
                expect(myth.mythVideos).to.satisfy(function (s) {
                    return s === null || Array.isArray(s)
                });
            });
        });
    });
});
