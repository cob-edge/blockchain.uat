const IoT = artifacts.require('./IoT.sol')

contract('IoT', (accounts) => {
  before(async () => {
    this.ioT = await IoT.deployed()
  })

  it('deploys successfully', async () => {
    const address = await this.ioT.address
    assert.notEqual(address, 0x0)
    assert.notEqual(address, '')
    assert.notEqual(address, null)
    assert.notEqual(address, undefined)
  })

    //here
  it('lists tasks', async () => {
    const taskCount = await this.ioT.taskCount()
    const task = await this.ioT.tasks(taskCount)
    assert.equal(task.id.toNumber(), taskCount.toNumber())
    assert.equal(task.timestamp, 'timestamp')
    assert.equal(task.desc, 'desc')
    assert.equal(task.entityType, 'entityType')
    assert.equal(task.v1.toNumber(), 1)
    assert.equal(task.v2.toNumber(), 1)
    assert.equal(task.v3.toNumber(), 1)
    assert.equal(task.latitude.toNumber(), 1)
    assert.equal(task.longitude.toNumber(), 1)
  })

    
    it('creates tasks', async () => {
        //readTextFile("file:///C:/Users/cob.edge.uat/source/repos/IoT-Simulator-Emulator-main/Dump%20Messages/14-08-2021_22_05_44.79544637.txt");

        for (var i = 2; i <= 1000; i++) {
            const result = await this.ioT.createTask(i, 'Timestamp: Today Baby Jarvis', 'Test desc', 'Test entity type', 1, 2, 3, 1, 2)

            /*
            const taskCount = await this.ioT.taskCount()
            assert.equal(taskCount, 2)
            const event = result.logs[0].args
            assert.equal(event.id.toNumber(), 2)
            assert.equal(event.timestamp, 'Timestamp: Today Baby Jarvis')
            assert.equal(event.desc, 'Test desc')
            assert.equal(event.entityType, 'Test entity type')
            assert.equal(event.v1.toNumber(), 1)
            assert.equal(event.v2.toNumber(), 2)
            assert.equal(event.v3.toNumber(), 3)
            assert.equal(event.latitude.toNumber(), 1)
            assert.equal(event.longitude.toNumber(), 2)
            */

            sleep(600) //introduced to stop ganache crashing 
        }
    })
})



function readTextFile(file) {
    var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function () {
        if (rawFile.readyState === 4) {
            if (rawFile.status === 200 || rawFile.status == 0) {
                var allText = rawFile.responseText;
                //alert(allText);
            }
        }
    }
    rawFile.send(null);
    console.log(rawFile.responseText)
}

function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
        currentDate = Date.now();
    } while (currentDate - date < milliseconds);
}
