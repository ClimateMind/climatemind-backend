export function generateFirstName(length) {
    var result = '';
    var characters = 'abcdefghijklmnopqrstuvwxyz';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() *
            charactersLength));
    }
    var capitaliseFirstLetter = result.charAt(0).toUpperCase() + result.slice(1);
    return capitaliseFirstLetter;
}

export function generateLastName(length) {
    var result = '';
    var characters = 'abcdefghijklmnopqrstuvwxyz';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() *
            charactersLength));
    }
    var capitaliseFirstLetter = result.charAt(0).toUpperCase() + result.slice(1);
    return capitaliseFirstLetter;
}
export function generateEmail(length) {
    var result = '';
    var characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() *
            charactersLength));
    }
    return result;
}

export function generatePassword(length) {
    const uppercase = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
    const lowecase = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"];
    const specialCharacters = ["~", "`", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", "|", "/", ":", ";", "<", ">", ".", "?"];
    const numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];

    var result = '';
    for (var i = 0; i < length; i++) {
        var uppercaseLetter = uppercase[Math.floor(Math.random() * uppercase.length)];
        var lowecaseLetter = lowecase[Math.floor(Math.random() * lowecase.length)];
        var aSpecialCharacter = specialCharacters[Math.floor(Math.random() * specialCharacters.length)];
        var aNumber = numbers[Math.floor(Math.random() * numbers.length)];
        result += uppercaseLetter + aNumber + lowecaseLetter + aSpecialCharacter
        if (result.length === length) break
    }
    return result;
}

export var randomFirstName = generateFirstName(5)
export var randomLastName = generateLastName(6)
export var randomEmail = generateEmail(5)
export var randomPassword = generatePassword(11)

export var user = {
    firstName: randomFirstName,
    lastName: randomLastName,
    email: `${randomEmail}@example.com`,
    password: randomPassword,
};
