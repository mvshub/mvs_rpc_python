import mvs_api

if __name__ == "__main__":
    err, ret = mvs_api.getdid()
    assert (err == None)
    print ret
    err, ret = mvs_api.getdid('ALICE.DIID')
    assert (err == None)
    print ret
    err, ret = mvs_api.getnewmultisig("Alice", "A123456", 2, 3, "0380990a7312b87abda80e5857ee6ebf798a2bf62041b07111287d19926c429d11",
                ["02578ad340083e85c739f379bbe6c6937c5da2ced52e09ac1eec43dc4c64846573", "03af3a99f1c3279dbe1c22fd767fb98b5dbd138f6e0511c2fc11128e44c0373cad"],
                 "test mvs api"                )
    assert (err == None)
    print ret
    ec, result = mvs_api.listmultisig("Alice", "A123456")
    assert (err == None)
    err, ret = mvs_api.deletemultisig("Alice", "A123456", result["multisig"][0]["address"])
    assert (err == None)
    print ret
    err, ret = mvs_api.getaccountasset("Alice", "A123456", cert=True)
    assert (err == None)
    print ret


    # special arguments in the cmd:
    # ['listtxs', 'importaccount', 'dumpkeyfile', 'listbalances', 'getasset', 'listassets', 'getaccountasset', 'getmit', 'getaddressasset', 'signmultisigtx']
    # listtxs
    err, ret = mvs_api.listtxs("Alice", "A123456", "MLasJFxZQnA49XEvhTHmRKi2qstkj9ppjo", (1000, 1001))
    assert (err == None)
    print ret

    # importaccount
    err, ret = mvs_api.importaccount("notice judge certain company novel quality plunge list blind library ride uncover fold wink biology original aim whale stand coach hire clinic fame robot".split(), "robot", "robot", hd_index= 10)
    assert (err == None)
    print ret

    err, ret = mvs_api.deleteaccount("robot", "robot", 'robot')
    assert (err == None)
    print ret

    # dumpkeyfile
    err, ret = mvs_api.dumpkeyfile("Alice", "A123456", "robot", data=True)
    assert (err == None)
    print ret

    # listbalances
    err, ret = mvs_api.listbalances("Alice", "A123456", nozero=True, greater_equal=10000, lesser_equal=10**9)
    assert (err == None)
    print ret

    # getasset
    err, ret = mvs_api.getasset(cert=True)
    assert (err == None)
    print ret

    err, ret = mvs_api.getasset(cert=False)
    assert (err == None)
    print ret

    err, ret = mvs_api.getasset()
    assert (err == None)
    print ret
