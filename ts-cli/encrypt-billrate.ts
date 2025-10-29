import * as crypto from 'crypto';

function pad(data: Buffer): Buffer {
  const padding = 16 - (data.length % 16);
  return Buffer.concat([data, Buffer.alloc(padding, padding)]);
}

function encryptBillRate(billRate: string, key: Buffer): string {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  const padded = pad(Buffer.from(billRate, 'utf-8'));
  const encrypted = Buffer.concat([cipher.update(padded), cipher.final()]);
  const blob = Buffer.concat([iv, encrypted]);
  return blob.toString('base64');
}

function main() {
  // Accept bill rate and key from command-line args or environment
  const billRate = process.argv[2] || process.env.BILL_RATE;
  const keyHex = process.argv[3] || process.env.AES_KEY_HEX;

  if (!billRate) {
    console.error('Bill rate must be provided as first argument or BILL_RATE env var.');
    process.exit(1);
  }
  if (!keyHex || keyHex.length !== 64) {
    console.error('Key must be provided as second argument or AES_KEY_HEX env var (64 hex characters).');
    process.exit(1);
  }
  const key = Buffer.from(keyHex, 'hex');
  const encrypted = encryptBillRate(billRate, key);
  console.log(encrypted);
}

main();
