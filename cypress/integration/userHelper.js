// import { faker } from "faker";
var faker = require("faker");

export function makeFakeUser() {
  const fakeUser = {
    firstName: faker.name.firstName(),
    lastName: faker.name.lastName(),
    email: faker.internet.email(),
    password: "PassWord7!",
  };
  return fakeUser;
}
