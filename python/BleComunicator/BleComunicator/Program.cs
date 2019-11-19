using System;
using Windows.Devices.Bluetooth.Advertisement;

public class Checker
{
    private readonly BluetoothLEAdvertisementWatcher mWatcher;
    public bool Listening => mWatcher.Status == BluetoothLEAdvertisementWatcherStatus.Started;

    public event Action StoppedListening = () => {};

    public event Action StartedListening = () => {};
    public Checker()
    {
        mWatcher = new BluetoothLEAdvertisementWatcher
        {
            ScanningMode = BluetoothLEScanningMode.Active
        };
        mWatcher.Received += CheckerReceived;
        mWatcher.Received += (watcher, e) =>
        {
            StoppedListening();
        };
    }
    private void CheckerReceived(BluetoothLEAdvertisementWatcher sender, BluetoothLEAdvertisementReceivedEventArgs args)
    {
        args.Advertisement.Lo == BluetoothLEAdvertisementFlags.
    }

    public void StartListening()
    {
        if (Listening)
            return;
        mWatcher.Start();
        StartedListening();
    }
    public void StopListening()
    {
        if (!Listening)
            return;
        mWatcher.Stop();
        StoppedListening();
    }
}
namespace BleComunicator
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello");
            var checker = new Checker();

            checker.StartedListening += () =>
            {
                Console.WriteLine("Started listening");
            };
            checker.StoppedListening += () =>
            {
                Console.WriteLine("Stopped listening");
            };
            checker.StartListening();
            Console.ReadLine();
        }
    }
}
