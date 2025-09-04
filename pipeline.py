write_dataframe(ws_ana, analysis)

    print("✅ Analysis refreshed!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--backfill', type=int, help='Fetch N days history and rebuild analysis.')
    parser.add_argument('--update-today', action='store_true', help='Fetch today and update analysis.')
    args = parser.parse_args()

    if args.backfill:
        backfill(args.backfill)
    elif args.update_today:
        update_today()
    else:
        print('Nothing to do. Use --backfill N or --update-today.')
