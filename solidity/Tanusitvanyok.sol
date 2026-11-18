// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @notice Tanusitvanyok lenyomatait tarolo szerzodes.
/// @dev Csak a kezelo szerzodes rogzithet uj lenyomatot.
contract TanusitvanyTarolo {
    address public immutable kezelo;
    mapping(bytes32 => bool) private letezoLenyomatok;
    uint256 public darabszam;

    event TanusitvanyRogzitve(bytes32 indexed lenyomat);

    constructor(address _kezelo) {
        require(_kezelo != address(0), "Ervenytelen kezelo");
        kezelo = _kezelo;
    }

    function rogzit(bytes32 lenyomat) external {
        require(msg.sender == kezelo, "Csak a kezelo hivhatja");
        require(!letezoLenyomatok[lenyomat], "Mar szerepel a taroloban");
        letezoLenyomatok[lenyomat] = true;
        darabszam += 1;
        emit TanusitvanyRogzitve(lenyomat);
    }

    function letezik(bytes32 lenyomat) external view returns (bool) {
        return letezoLenyomatok[lenyomat];
    }
}

/// @notice Egyszeru felulet a tanusitvanyok regisztralasahoz es ellenorzesehez.
/// @dev Oktatasi pelda. A szoveg nem tarolodik, csak a keccak256 lenyomata.
contract TanusitvanyKezelo {
    TanusitvanyTarolo public immutable tarolo;

    constructor() {
        tarolo = new TanusitvanyTarolo(address(this));
    }

    function regisztral(string calldata tanusitvany) external {
        require(bytes(tanusitvany).length > 0, "Ures szoveg nem engedelyezett");
        bytes32 lenyomat = keccak256(bytes(tanusitvany));
        tarolo.rogzit(lenyomat); // Az egyik okosszerzodes meghivja a masikat.
    }

    function ellenoriz(string calldata tanusitvany) external view returns (bool) {
        bytes32 lenyomat = keccak256(bytes(tanusitvany));
        return tarolo.letezik(lenyomat);
    }

    function lenyomat(string calldata tanusitvany) external pure returns (bytes32) {
        return keccak256(bytes(tanusitvany));
    }

    function regisztraciokSzama() external view returns (uint256) {
        return tarolo.darabszam();
    }
}
