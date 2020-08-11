import unittest

from unittest import IsolatedAsyncioTestCase
from pyfreenas import Controller
from pyfreenas.virtualmachine import VirturalMachine, VirturalMachineState
from tests.fakes.fakeserver import FreeNASServer


class TestVirturalMachine(IsolatedAsyncioTestCase):
    _server: FreeNASServer
    _controller: Controller

    def setUp(self):
        self._server = FreeNASServer()
        self._server.register_method_handler(
            "disk.query", lambda *args: [],
        )
        self._server.register_method_handler(
            "disk.temperatures", lambda *args: {},
        )

    async def asyncSetUp(self):
        self._controller = await Controller.create(
            self._server.host,
            username=self._server.username,
            password=self._server.password,
        )

    async def asyncTearDown(self):
        await self._controller.close()
        await self._server.stop()

    async def test_running_data_interpretation(self) -> None:
        DESCRIPTION = "Some Desc"
        ID = 1
        NAME = "vm01"
        self._server.register_method_handler(
            "vm.query",
            lambda *args: [
                {
                    "description": DESCRIPTION,
                    "id": ID,
                    "name": NAME,
                    "status": {"pid": 42, "state": "RUNNING"},
                },
            ],
        )

        await self._controller.refresh()

        self.assertEqual(len(self._controller.vms), 1)
        vm = self._controller.vms[0]
        self.assertEqual(vm.description, DESCRIPTION)
        self.assertEqual(vm.id, ID)
        self.assertEqual(vm.name, NAME)
        self.assertEqual(vm.status, VirturalMachineState.RUNNING)

    async def test_stopped_data_interpretation(self) -> None:
        DESCRIPTION = ""
        ID = 3
        NAME = "vm02"
        self._server.register_method_handler(
            "vm.query",
            lambda *args: [
                {
                    "description": DESCRIPTION,
                    "id": ID,
                    "name": NAME,
                    "status": {"pid": None, "state": "STOPPED"},
                },
            ],
        )

        await self._controller.refresh()

        self.assertEqual(len(self._controller.vms), 1)
        vm = self._controller.vms[0]
        self.assertEqual(vm.description, DESCRIPTION)
        self.assertEqual(vm.id, ID)
        self.assertEqual(vm.name, NAME)
        self.assertEqual(vm.status, VirturalMachineState.STOPPED)

    async def test_availability(self) -> None:
        self._server.register_method_handler(
            "vm.query",
            lambda *args: [
                {
                    "description": "Some Desc",
                    "id": 1,
                    "name": "vm01",
                    "status": {"pid": 42, "state": "RUNNING"},
                },
            ],
        )

        await self._controller.refresh()

        vm = self._controller.vms[0]
        self.assertTrue(vm.available)

        self._server.register_method_handler(
            "vm.query", lambda *args: [], override=True,
        )
        await self._controller.refresh()
        self.assertFalse(vm.available)

    async def test_unavailable_caching(self) -> None:
        """Certain properites have caching even if no longer available"""
        DESCRIPTION = "Some Desc"
        ID = 1
        NAME = "vm01"
        self._server.register_method_handler(
            "vm.query",
            lambda *args: [
                {
                    "description": DESCRIPTION,
                    "id": ID,
                    "name": NAME,
                    "status": {"pid": 42, "state": "RUNNING"},
                },
            ],
        )
        await self._controller.refresh()
        vm = self._controller.vms[0]
        assert vm is not None
        self._server.register_method_handler(
            "vm.query", lambda *args: [], override=True,
        )
        await self._controller.refresh()

        self.assertEqual(vm.description, DESCRIPTION)
        self.assertEqual(vm.id, ID)
        self.assertEqual(vm.name, NAME)
        with self.assertRaises(AssertionError):
            vm.status


if __name__ == "__main__":
    unittest.main()
