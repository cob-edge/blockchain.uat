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
    assert.equal(task.timestamp, 'Timestamp: Today Baby Jarvis')
    assert.equal(task.desc, 'Test desc')
    assert.equal(task.entityType, 'Test entity type')
    assert.equal(task.v1.toNumber(), 1)
    assert.equal(task.v2.toNumber(), 2)
    assert.equal(task.v3.toNumber(), 3)
    assert.equal(task.latitude.toNumber(), 1)
    assert.equal(task.longitude.toNumber(), 2)
  })

  
    it('creates tasks', async () => {
    const result = await this.ioT.createTask(2, 'Timestamp: Today Baby Jarvis', 'Test desc', 'Test entity type', 1, 2, 3, 1, 2)

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
  }) 

})
